# <<BEGIN-copyright>>
# Copyright (c) 2011, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
# Written by the LLNL Computational Nuclear Physics group
#         (email: mattoon1@llnl.gov)
# LLNL-CODE-494171 All rights reserved.
# 
# This file is part of the FUDGE package (For Updating Data and 
#         Generating Evaluations)
# 
# When citing FUDGE, please use the following reference:
#   C.M. Mattoon, B.R. Beck, N.R. Patel, N.C. Summers, G.W. Hedstrom, D.A. Brown, "Generalized Nuclear Data: A New Structure (with Supporting Infrastructure) for Handling Nuclear Data", Nuclear Data Sheets, Volume 113, Issue 12, December 2012, Pages 3145-3171, ISSN 0090-3752, http://dx.doi.org/10. 1016/j.nds.2012.11.008
# 
# 
#     Please also read this link - Our Notice and Modified BSD License
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of Lawrence Livermore National Security, LLC. nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL LAWRENCE LIVERMORE NATIONAL SECURITY BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# <<END-copyright>>

from fudge.gnd import baseClasses
import base
from fudge.gnd import tokens

__metaclass__ = type

#
# fissionEnergyReleased genre and forms
#
class component( baseClasses.componentBase ) :

    genre = base.fissionEnergyReleasedToken

    def __init__( self ) :

        baseClasses.componentBase.__init__( self )

    def check( self, info ) :

        from fudge.gnd import warning
        warnings = []
        for form in self.forms:
            fwarnings = self.forms[form].check( info )
            if fwarnings:
                warnings.append( warning.context('%s:' % form, fwarnings) )
        return warnings

    @staticmethod
    def parseXMLNode( FERelement, xPath, linkData ):
        """ parse <fissionEnergyReleased> from xml """

        xPath.append( FERelement.tag )
        fer = component()
        for form in FERelement:
            if form.tag==tokens.polynomialFormToken:
                fer.addForm( polynomial.parseXMLNode( form, xPath, linkData ) )
        xPath.pop()
        return fer

class polynomial( baseClasses.formBase ) :

    genre = component.genre
    moniker = tokens.polynomialFormToken

    labels = [ 'promptProductKE', 'promptNeutronKE', 'delayedNeutronKE', 'promptGammaEnergy', 'delayedGammaEnergy', 'delayedBetaEnergy', 'neutrinoEnergy',
                'nonNeutrinoEnergy', 'totalEnergy' ]

    def __init__( self, label, order, data, energyUnit, hasUncertainties = False ) :

        self.order = order
        self.data = data
        self.energyUnit = energyUnit                        # Need to use this in toENDF6.
        self.hasUncertainties = hasUncertainties

        if( label is not None ) :
            if( not( isinstance( label, str ) ) ) : raise TypeError( 'label must be a string' )
        self.__label = label

    def check( self, info ):

        from fudge.gnd import warning
        from pqu import PQU
        warnings = []
        domain = [d.getValueAs( self.energyUnit ) for d in info['crossSectionDomain']]
        for key in self.data:   # 'totalEnergy', 'nonNeutrinoEnergy', etc
            coefs = [a[0] for a in self.data[key]]
            poly = lambda e: sum( [coef * e**i for i,coef in enumerate(coefs)] )
            for ein in domain:
                if not 0 < poly(ein) < 4e+8: # 0 MeV -> 400 MeV considered acceptable
                    warnings.append( warning.badFissionEnergyRelease( key, PQU.PQU(ein,self.energyUnit), 
                        PQU.PQU(poly(ein),self.energyUnit) ) )
        return warnings

    @property
    def label( self ) :

        return( self.__label )

    @staticmethod
    def parseXMLNode( element, xPath, linkData ):
        """ translate <polynomial> element from xml """

        xPath.append( element.tag )
        order = int( element.get("order") )
        hasUncertainties = False
        dataDict = {}
        for data in element:
            coefs = map(float, data.text.split())
            if len(coefs) == (order+1)*2:
                hasUncertainties=True
                coefs = zip( coefs[::2], coefs[1::2] )
            assert len(coefs) == order+1
            dataDict[data.tag] = coefs
        Poly = polynomial( element.get('label'), order, dataDict, element.get('energyUnit'), hasUncertainties )
        xPath.pop()
        return Poly

    def toXMLList( self, indent = "", **kwargs ) :

        indent2 = indent + kwargs.get( 'incrementalIndent', '  ' )

        hasUncertainties = ''
        if( self.hasUncertainties ) : hasUncertainties = ' hasUncertainties="true"'
        xmlString = [ '%s<%s label="%s" order="%s" energyUnit="%s"%s>' % ( indent, self.moniker,
                                                    self.label, self.order, self.energyUnit, hasUncertainties ) ]
        for label in self.labels :
            data = ""
            for d in self.data[label] :
                for v in d : data += ' %s' % v
            xmlString.append( '%s<%s>%s</%s>' % ( indent2, label, data, label ) )
        xmlString[-1] += '</%s>' % self.moniker
        return( xmlString )
