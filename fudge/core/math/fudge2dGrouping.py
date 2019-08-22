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
# 
#     Please also read this link - Our Notice and GNU General Public License.
# 
# This program is free software; you can redistribute it and/or modify it under 
# the terms of the GNU General Public License (as published by the Free Software
# Foundation) version 2, dated June 1991.
# This program is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF MERCHANTABILITY 
# or FITNESS FOR A PARTICULAR PURPOSE. See the terms and conditions of 
# the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with 
# this program; if not, write to 
# 
# the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330,
# Boston, MA 02111-1307 USA
# <<END-copyright>>

import copy
from fudge.core import fudgemisc
numpyImported = False
try :
    import numpy
    numpyImported = True
except :
    fudgemisc.printWarning( "Warning from fudge2dGrouping.py: numpy not imported" )

__metaclass__ = type

class groupedData :

    def __init__( self, data, axes_ = None ) :

        if( axes_ is not None ) :
            self.axes = axes_
        elif( hasattr( data, 'axes' ) ) :
            self.axes = data.axes
        if( len( data ) == 0 ) :
            self.start = 0
            self.end = 0
        else :
            i = 0
            self.end = 0
            for x in data :
                if( x != 0. ) : self.end = i
                i += 1
            if( data[self.end] != 0. ) : self.end += 1
            if( self.end == 0 ) :
                self.start = 0
            else :
                i = 0
                for x in data :
                    if( x != 0. ) : break
                    i += 1
                self.start = i
        self.data = data

    def __str__( self ) :

        return( self.toString( ) )

    def __getitem__( self, i ) :
        """Returns the (i+1)^th element of self."""

        return( self.data[i] )

    def __setitem__( self, i, value ) :
        """Sets the (i+1)^th element of self to value."""

        self.data[i] = value

    def __len__( self ) :
        """Returns the number of data points in self."""

        return( len( self.data ) )

    def __add__( self, other ) :
        """Adds every element of self and other. Other must be a number or another instance of groupedData class."""

        if( ( type( other ) == type( 1 ) ) or ( type( other ) == type( 1. ) ) ) : 
            new = groupedData( copy.copy( self.data ) )
            for i in xrange( len( self ) ) : new.data[i] += other
        elif( isinstance( other, groupedData ) ) :
            new = groupedData( copy.copy( self.data ) )
            for i, d in enumerate( other.data ) : new.data[i] += d
            new.start, new.end = min( self.start, other.start ), max( self.end, other.end )
        else :
            raise Exception( 'other not a number or instance of groupedData. Type( other ) = %s' % `type( other )` )
        return( new )

    def __sub__( self, other ) :
        """Substracts every element of other from self. Other must be a number or another instance of groupedData class."""

        if( ( type( other ) == type( 1 ) ) or ( type( other ) == type( 1. ) ) ) : 
            new = groupedData( copy.copy( self.data ) )
            for i in xrange( len( self ) ) : new.data[i] -= other
        elif( isinstance( other, groupedData ) ) :
            new = groupedData( copy.copy( self.data ) )
            for i, d in enumerate( other.data ) : new.data[i] -= d
            new.start, new.end = min( self.start, other.start ), max( self.end, other.end )
        else :
            raise Exception( 'other not a number or instance of groupedData. Type( other ) = %s' % `type( other )` )
        return( new )

    def __mul__( self, other ) :
        """Multiplies every element of self by other. Other must be a number."""

        if( ( type( other ) != type( 1 ) ) and ( type( other ) != type( 1. ) ) ) : 
            raise Exception( 'other not a number. Type( other ) = %s' % `type( other )` )
        data = []
        for d in self : data.append( d * other )
        return( groupedData( data ) )

    def __rmul__( self, other ) :
        """See __mul__."""

        return( self.__mul__( other ) )

    def getData( self ) :
        """Returns the data of self."""

        return( self.data )

    def getEnd( self ) :
        """Returns the index of the last non-zero data in self."""

        return( self.end )

    def getStart( self ) :
        """Returns the index of the first non-zero data in self."""

        return( self.start )

    def toString( self ) :

        s = [ 'length = %d, start = %d, end = %d' % ( len( self ), self.start, self.end ) ]
        for i in xrange( self.start, self.end ) : s.append( '%15.8e' % self.data[i] )
        s.append( '' )
        return( '\n'.join( s ) )

    def toXMLList( self, indent = "", floatFormat = '%16.9e' ) :

        tag, indent2, sizeStr, start, end = 'grouped', indent + '  ', '', self.getStart( ), self.getEnd( )
        if( hasattr( self, 'tag' ) ) : tag = self.tag
        if( start != 0 ) : sizeStr = ' start="%d"' % start
        if( end < len( self ) ) : sizeStr += ' end="%d"' % end
        xmlString = [ '%s<%s xData="groupedY" nGroups="%i"%s>' % ( indent, tag, len(self.data), sizeStr )
                    ] + self.axes.toXMLList( indent = indent2 )
        data = []
        for i, y in enumerate( self.data ) :
            if( i < start ) : continue
            if( i >= end ) : break
            data.append( floatFormat % y )
        xmlString.append( '%s<data>%s</data>' % ( indent2, ' '.join( data ) ) )
        xmlString[-1] += '</%s>' % tag
        return( xmlString )

    @classmethod
    def parseXMLNode( cls, element, xPath=[], linkData={} ):
        xPath.append( element.tag )
        from fudge.core.math.xData import axes
        axes_ = axes.parseXMLNode( element[0] )
        nGroups = int( element.get('nGroups') )
        start, end = 0, nGroups
        if element.get('start') is not None: start = int( element.get('start') )
        if element.get('end') is not None: end = int( element.get('end') )
        data = [0] * nGroups
        if element[1].text:
            data[start:end] = map(float, element[1].text.split())
        grouped_ = cls( axes_, data )
        xPath.pop()
        return grouped_
