# <<BEGIN-copyright>>
# Copyright 2022, Lawrence Livermore National Security, LLC.
# See the top-level COPYRIGHT file for details.
# 
# SPDX-License-Identifier: BSD-3-Clause
# <<END-copyright>>

"""This module defines the Yields, Values, Uncertainty, Covariance and NuclidesLink classes,
used to store the fission product yield values and uncertainties corresponding to a set of Nuclides.

For spontaneous fission, a **Yields** class is stored for each **ElapsedTime**."""

from LUPY import ancestry as ancestryModule

from xData import link as linkModule
from xData import xDataArray as arrayModule

from .. import misc as miscModule
from . import nuclides as nuclidesModule

class NuclidesLink(linkModule.Link):

    moniker = 'nuclides'

class Values(miscModule.ClassWithLabelKey):
    """Stores a list of fission product yield values. The length and order must be consistent
    with the corresponding **Nuclides** list."""

    moniker = 'values'

    def __init__(self, _values):
        """Construct a **Values** instance.

        :param _values: list of floating-point fission product yields."""

        miscModule.ClassWithLabelKey.__init__(self, 'label')
        self.__values = tuple(float(value) for value in _values)

    def __getitem__(self, index):

        return self.__values[index]

    def __iter__(self):

        # FIXME CMM why iterate by index?
        n1 = len(self.__values)
        for i1 in range(n1): yield self.__values[i1]

    def toXML_strList(self, indent = '', **kwargs):
        """
        Returns a list of str instances representing the XML lines of self.

        :param indent:    The amount of indentation for each line. Child nodes and text may be indented more.
        :param kwargs:    A keyword list.

        :return:          List of str instances representing the XML lines of self.
        """

        indent2 = indent + kwargs.get( 'incrementalIndent', '  ' )

        XMLStringList = [ '%s<%s>' % (indent, self.moniker) ]
        XMLStringList[-1] += ' '.join([ '%s' % value for value in self.__values ])
        XMLStringList[-1] += '</%s>' % self.moniker

        return XMLStringList

    @classmethod
    def parseNodeUsingClass(cls, node, xPath, linkData, **kwargs):
        """Create a new instance of class **cls** and parse contents of node into the instance.

        :param cls: FUDGE Python class to return.
        :param node: **values** node to parse.
        :param xPath: List containing xPath to current node, useful mostly for debugging.
        :param linkData: dict that collects unresolved links.
        """

        xPath.append( node.tag )
        values_ = cls( map(float, node.text.split()) )
        xPath.pop()
        return values_

class Covariance(ancestryModule.AncestryIO):
    """Class storing the fission product yield covariance matrix. If yields are given for N nuclides,
    the matrix has dimension NxN and correlates the yields for outgoing nuclide at the given elapsed time."""

    moniker = 'covariance'

    def __init__(self, _matrix):

        ancestryModule.AncestryIO.__init__(self)
        self.__matrix = _matrix

    def matrix(self):

        return self.__matrix

    def toXML_strList(self, indent = '', **kwargs):
        """
        Returns a list of str instances representing the XML lines of self.

        :param indent:    The amount of indentation for each line. Child nodes and text may be indented more.
        :param kwargs:    A keyword list.

        :return:          List of str instances representing the XML lines of self.
        """

        indent2 = indent + kwargs.get('incrementalIndent', '  ')

        if 'valuesPerLine' not in kwargs: kwargs['valuesPerLine'] = 1000
        XMLStringList = [ '%s<%s>' % (indent, self.moniker) ]
        XMLStringList += self.__matrix.toXML_strList(indent2, **kwargs)
        XMLStringList[-1] += '</%s>' % self.moniker

        return XMLStringList

    @classmethod
    def parseNodeUsingClass(cls, node, xPath, linkData, **kwargs):
        """Create a new instance of class **cls** and parse contents of node into the instance.

        :param cls: FUDGE Python class to return.
        :param node: **covariance** node to parse.
        :param xPath: List containing xPath to current node, useful mostly for debugging.
        :param linkData: dict that collects unresolved links.
        """
        xPath.append(node.tag)
        child = node[0]
        if child.tag == arrayModule.ArrayBase.moniker:
            _matrix = arrayModule.ArrayBase.parseNodeUsingClass(child, xPath, linkData, **kwargs)
        else:
            raise TypeError("Unexpected child node '%s' in %s" % (child.tag, node.tag))
        covar_ = cls(_matrix)
        xPath.pop()
        return covar_

class Uncertainty(ancestryModule.AncestryIO):
    """Class containing the fission product yield uncertainty. Uncertainty could be stored various ways,
    but in practice it is currently always stored as a covariance matrix (although the matrix typically
    has no non-zero terms off the diagonal."""

    moniker = 'uncertainty'

    def __init__(self, form):

        ancestryModule.AncestryIO.__init__(self)

        self.__form = form

    def form(self):
        """Return the uncertainty form, typically a Covariance instance."""

        return self.__form

    def toXML_strList(self, indent = '', **kwargs):
        """
        Returns a list of str instances representing the XML lines of self.

        :param indent:    The amount of indentation for each line. Child nodes and text may be indented more.
        :param kwargs:    A keyword list.

        :return:          List of str instances representing the XML lines of self.
        """

        indent2 = indent + kwargs.get('incrementalIndent', '  ')

        XMLStringList = [ '%s<%s>' % (indent, self.moniker) ]
        XMLStringList += self.__form.toXML_strList(indent2, **kwargs)
        XMLStringList[-1] += '</%s>' % self.moniker

        return XMLStringList

    @classmethod
    def parseNodeUsingClass(cls, node, xPath, linkData, **kwargs):
        """Create a new instance of class **cls** and parse contents of node into the instance.

        :param cls: FUDGE Python class to return.
        :param node: **Uncertainty** node to parse.
        :param xPath: List containing xPath to current node, useful mostly for debugging.
        :param linkData: dict that collects unresolved links.
        """
        xPath.append(node.tag)
        child = node[0]
        if child.tag == Covariance.moniker:
            form = Covariance.parseNodeUsingClass(child, xPath, linkData, **kwargs)
        else:
            raise TypeError("Unexpected child node '%s' in %s" % (child.tag, node.tag))
        uncert_ = cls(form)
        xPath.pop()
        return uncert_

class Yields(ancestryModule.AncestryIO):
    """Class storing product yields for an elapsed time. Class contains a list of nuclides (may be a link),
    a list of values storing the product yield for each nuclide, and an optional uncertainty."""

    moniker = 'yields'

    def __init__(self):

        ancestryModule.AncestryIO.__init__(self)

        self.__nuclides = None
        self.__values = None
        self.__uncertainty = None

    @property
    def nuclides(self):
        """Return the list of nuclides, or a link if the nuclides are defined elsewhere."""

        return self.__nuclides

    @nuclides.setter
    def nuclides(self, value):

        if not isinstance(value, (NuclidesLink, nuclidesModule.Nuclides)):
            raise TypeError( 'Invalid nuclides instance.' )
        self.__nuclides = value
        self.__nuclides.setAncestor(self)

    @property
    def values(self):
        """Return the fission product yield values."""

        return self.__values

    @values.setter
    def values(self, _values):

        if not isinstance(_values, Values): raise TypeError('Invalid values instance.')
        self.__values = _values
        self.__values.setAncestor(self)

    @property
    def uncertainty(self):
        """Return the fission product yield uncertainty (may be None)."""

        return self.__uncertainty

    @uncertainty.setter
    def uncertainty(self, _uncertainty):

        if not isinstance(_uncertainty, Uncertainty): raise TypeError('Invalid Uncertainty instance.')
        self.__uncertainty = _uncertainty
        self.__uncertainty.setAncestor(self)

    def toXML_strList(self, indent = '', **kwargs):
        """
        Returns a list of str instances representing the XML lines of self.

        :param indent:    The amount of indentation for each line. Child nodes and text may be indented more.
        :param kwargs:    A keyword list.

        :return:          List of str instances representing the XML lines of self.
        """

        indent2 = indent + kwargs.get('incrementalIndent', '  ')

        XMLStringList = [ '%s<%s>' % (indent, self.moniker) ]
        if self.__nuclides is not None: XMLStringList += self.__nuclides.toXML_strList(indent2, **kwargs)
        if self.__values is not None: XMLStringList += self.__values.toXML_strList(indent2, **kwargs)
        if self.__uncertainty is not None: XMLStringList += self.__uncertainty.toXML_strList(indent2, **kwargs)
        XMLStringList[-1] += '</%s>' % self.moniker

        return XMLStringList

    def parseNode(self, node, xPath, linkData, **kwargs):

        xPath.append(node.tag)
        for child in node:
            if child.tag == NuclidesLink.moniker:
                if child.get('href') is not None:
                    self.nuclides = NuclidesLink.parseNodeUsingClass(child, xPath, linkData, **kwargs)
                else:
                    self.nuclides = nuclidesModule.Nuclides.parseNodeUsingClass(child, xPath, linkData, **kwargs)
            elif child.tag == Values.moniker:
                self.values = Values.parseNodeUsingClass(child, xPath, linkData, **kwargs)
            elif child.tag == Uncertainty.moniker:
                self.uncertainty = Uncertainty.parseNodeUsingClass(child, xPath, linkData, **kwargs)
            else:
                raise TypeError("Unexpected child node '%s' in %s" % (child.tag, node.tag))

        xPath.pop()
        return self

    @classmethod
    def parseNodeUsingClass(cls, node, xPath, linkData, **kwargs):
        """Create a new instance of class **cls** and parse contents of node into the instance.

        :param cls: FUDGE Python class to return.
        :param node: **yields** node to parse.
        :param xPath: List containing xPath to current node, useful mostly for debugging.
        :param linkData: dict that collects unresolved links.
        """

        xPath.append(node.tag)
        self = cls()
        xPath.pop()
        self.parseNode(node, xPath, linkData, **kwargs)

        return self
