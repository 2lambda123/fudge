# <<BEGIN-copyright>>
# <<END-copyright>>

"""
This module contains the class V_W_XYs. This class treats a list of (v_i, w_xys) pairs as if they were the function w_xys(v)
where w_xys is an instance of class W_XYs.

    axes            Description of the v, w, x and y data attributes (e.g., label, interpolation, units).
"""

monikerV_W_XYs = 'V_W_XYs'

noExtrapolationToken = 'noExtrapolation'
flatExtrapolationToken = 'flatExtrapolation'

import axes, XYs, W_XYs
from fudge.core.ancestry import ancestry
from pqu import physicalQuantityWithUncertainty
from fudge.core.math import fudgemath
from fudge.core.utilities import brb, subprocessing

__metaclass__ = type

class V_W_XYs( ancestry ) :

    type = monikerV_W_XYs
    xData = monikerV_W_XYs

    def __init__( self, axes_, index = None, value = None, parent = None ) :

        attribute = None
        if( parent is not None ) :
            attribute = 'index'
            if( index is None ) : raise Exception( 'index argument cannot be None when parent is not None' )
        ancestry.__init__( self, self.type, parent, attribute = attribute )

        axes.isValidAxes( axes_ )
        axes_.checkDimension( 4 )

        self.w_xys = []
        self.axes = axes_.copy( )           # Even secondary must have axes
        self.index = index
        self.value = value

    def __len__( self ) :

        return( len( self.w_xys ) )

    def __getitem__( self, index ) :

        return( self.w_xys[index] )

    def __setitem__( self, index, w_xys_ ) :

        if( not( isinstance( w_xys_, W_XYs.W_XYs ) ) ) : raise Exception( 'right-hand-side must be instance of W_XYs; it is %s' % brb.getType( w_xys_ ) )
        if( type( w_xys_.value ) != type( 1. ) ) : raise Exception( 'w_xys value must be a float; it is a %s' % brb.getType( w_xys_.value ) )
        n = len( self )
        if( n < index ) : raise IndexError( 'index = %s while length is %s' % ( index, n ) )
        if( index < 0 ) : raise IndexError( 'index = %s' % index )
        w_xys = w_xys_.copy( parent = self, index = index, value = w_xys_.value, axes = axes.referenceAxes( self, dimension = 3 ), isPrimaryXData = False )
        if( n == 0 ) :
            self.w_xys.append( w_xys )
        elif( n == index ) :
            if( w_xys_.value <= self.w_xys[-1].value ) : raise Exception( 'w_xys.value = %s is <= prior w_xys.value = %s' % ( w_xys_.value, self.w_xys[-1].value ) )
            self.w_xys.append( w_xys )
        else :
            if( index > 0 ) :
                if( w_xys_.value <= self.w_xys[index - 1].value ) : 
                    raise Exception( 'w_xys.value = %s is <= prior w_xys.value = %s' % ( w_xys_.value, self.w_xys[index - 1].value ) )
            if( index < ( n - 1 ) ) :
                if( w_xys_.value >= self.w_xys[index + 1].value ) :
                    raise Exception( 'w_xys.value = %s is >= next w_xys.value = %s' % ( w_xys_.value, self.w_xys[index + 1].value ) )
            self.w_xys[index] = w_xys

    def append( self, w_xys_ ) :

        self[len( self )] = w_xys_

    def copy( self, index = None, value = None, parent = None ) :

        if( index is None ) : index = self.index
        if( value is None ) : value = self.value
        n = V_W_XYs( self.axes, index = index, value = value, parent = parent )
        for i, w_xys in enumerate( self ) : n[i] = w_xys        # A copy of w_xys is made by __setitem__.
        return( n )

    def interpolateAtV( self, v, unitBase = False, extrapolation = noExtrapolationToken ) :
        """Returns the interpolation of two XYs, xys1 and xys2, at v as a list of [x,y] pairs where wl = xys1.value <= w <= xys2.value = wu.
        If w is outside the domain of wl to wu, are raise is executed. Linear interpolation is performed on the xy data.  If unitBase is
        True, then unit base interpolation is performed."""

        if( len( self ) == 0 ) : raise Exception( "No data to interpolate" )
        if( v < self[0].value ) :
            if( extrapolation == flatExtrapolationToken ) :
                return( self[0].copy( ) )
            else :
                raise Exception( "Interpolation point = %s less than %s" % ( v, self[0].value ) )
        if( v > self[-1].value ) :
            if( extrapolation == flatExtrapolationToken ) :
                return( self[-1].copy( ) )
            else :
                raise Exception( "Interpolation point = %s greater than %s" % ( v, self[-1].value ) )
        for index, wxy2 in enumerate( self ) :
            if( wxy2.value >= v ) : break
        if( v == wxy2.value ) : return( wxy2.copy( ) )
        wxy1 = self[index-1]
        ws = [ xy.value for xy in wxy1 ]
        for xy in wxy2 :
            if( xy.value not in ws ) : ws.append( xy.value )
        ws.sort( )
        wxy_At_v = W_XYs.W_XYs( wxy1.axes, value = v )
        for iw, w in enumerate( ws ) :
            xy1 = wxy1.interpolateAtW( w, unitBase = False )
            xy2 = wxy2.interpolateAtW( w, unitBase = False )
            if( unitBase ) :
                xy = XYs.pointwiseXY_C.unitbaseInterpolate( v, wxy1.value, xy1, wxy2.value, xy2 )
            else :
                f = ( wxy2.value - v ) / ( wxy2.value - wxy1.value )
                xy = f * xy1 + ( 1. - f ) * xy2
            xyp = wxy1[0].copy( value = w )
            xyp.setData( xy )
            wxy_At_v[iw] = xyp
        return( wxy_At_v )

    def plot( self, vMin = None, vMax = None, wMin = None , wMax = None, xMin = None , xMax = None, yMin = None , yMax = None, xyzlog = 0, title = '' ) :

        from fudge.core import fudgemisc
        from fudge.core.utilities import fudgeFileMisc
        from fudge.vis.gnuplot import plotbase
        import os

        def getUnitlessNumber( value, unit, default ) :

            if( value is None ) : value = default
            if( fudgemath.isNumber( value ) ) : return( float( value ) )
            if( type( '' ) == type( value ) ) :
                try :
                    return( float( value ) )
                except :
                    value = physicalQuantityWithUncertainty.PhysicalQuantityWithUncertainty( value )
            if( isinstance( value, physicalQuantityWithUncertainty.PhysicalQuantityWithUncertainty ) ) : return( value.getValueAs( unit ) )
            raise Exception( 'Cannot convert %s to a unitless number' % str( value ) )

        vLabel = self.axes[0].plotLabel( )
        wLabel = self.axes[1].plotLabel( )
        xLabel = self.axes[2].plotLabel( )
        yLabel = self.axes[3].plotLabel( )

        wMin = getUnitlessNumber( wMin, self.axes[1].getUnit( ), self[0][0].value )
        wMax = getUnitlessNumber( wMax, self.axes[1].getUnit( ), self[0][0].value )
        xMin = getUnitlessNumber( xMin, self.axes[1].getUnit( ), self[0][0].xMin( ) )
        xMax = getUnitlessNumber( xMax, self.axes[1].getUnit( ), self[0][0].xMax( ) )
        yMin = getUnitlessNumber( yMin, self.axes[1].getUnit( ), self[0][0].yMin( ) )
        yMax = getUnitlessNumber( yMax, self.axes[1].getUnit( ), self[0][0].yMax( ) )
        for w_xys in self :
            wMin = min( wMin, w_xys.domainMin( ) )
            wMax = max( wMax, w_xys.domainMax( ) )
            for xys in w_xys :
                xMin = min( xMin, xys.xMin( ) )
                xMax = max( xMax, xys.xMax( ) )
                yMin = min( yMin, xys.yMin( ) )
                yMax = max( yMax, xys.yMax( ) )

        dt = plotbase.parsePlotOptions( wMin, wMax, xMin, xMax, wLabel, xLabel, title, zMin = yMin, zMax = yMax, zLabel = yLabel, tLabel = vLabel )
        f = fudgeFileMisc.fudgeTempFile( )
        f.write( self.toString( ) )
        f.close( )
        p = os.path.join( __file__.split( '/fudge/core/' )[0], "fudge", "vis", "gnuplot", "endl4dplot.py" )
        s = [ 'python', p, 'xyzlog', str( xyzlog ) ] + dt + [ f.getName( ) ]
        subprocessing.spawn( s )

    def domainUnitConversionFactor( self, unitTo ) :

        if( unitTo is None ) : return( 1. )
        return( physicalQuantityWithUncertainty.PhysicalQuantityWithUncertainty( '1 ' + self.getDomainUnit( ) ).getValueAs( unitTo ) )

    def domainMin( self, unitTo = None, asPQU = False ) :

        return( physicalQuantityWithUncertainty.valueOrPQ( self.w_xys[0].value, unitFrom = self.axes[0].getUnit( ), unitTo = unitTo, asPQU = asPQU ) )

    def domainMax( self, unitTo = None, asPQU = False ) :

        return( physicalQuantityWithUncertainty.valueOrPQ( self.w_xys[-1].value, unitFrom = self.axes[0].getUnit( ), unitTo = unitTo, asPQU = asPQU ) )

    def getDomain( self, unitTo = None, asPQU = False ) :

        return( self.domainMin( unitTo = unitTo, asPQU = asPQU ), self.domainMax( unitTo = unitTo, asPQU = asPQU ) )

    def getDomainGrid( self, unitTo = None ) :

        scale = self.domainUnitConversionFactor( unitTo )
        return( [ scale * w_xys.value for w_xys in self ] )

    def getDomainUnit( self ) :

        return( self.axes[0].getUnit( ) )

    def toPointwiseLinear( self, accuracy = None, lowerEps = 0, upperEps = 0, cls = None ) :

        from fudge.core.utilities import mathMisc

        axes_ = self.axes.copy( )
        independent, dependent, qualifier = self.axes[0].interpolation.getInterpolationTokens( )
        if( independent not in [ axes.linearToken ] ) : raise Exception( 'vy independent interpolation = %s not supported' % independent )
        if( dependent not in [ axes.linearToken ] ) : raise Exception( 'vy dependent interpolation = %s not supported' % dependent )
        axes_[0].setInterpolation( axes.interpolationXY( axes.linearToken, axes.linearToken, qualifier ) )

        independent, dependent, qualifier = self.axes[1].interpolation.getInterpolationTokens( )
        if( independent not in [ axes.linearToken ] ) : raise Exception( 'wy independent interpolation = %s not supported' % independent )
        if( dependent not in [ axes.linearToken ] ) : raise Exception( 'wy dependent interpolation = %s not supported' % dependent )
        axes_[1].setInterpolation( axes.interpolationXY( axes.linearToken, axes.linearToken, qualifier ) )

        independent, dependent, qualifier = self.axes[2].interpolation.getInterpolationTokens( )
        if( independent not in [ axes.linearToken ] ) : raise Exception( 'xy independent interpolation = %s not supported' % independent )
        if( dependent not in [ axes.linearToken ] ) : raise Exception( 'xy dependent interpolation = %s not supported' % dependent )
        axes_[2].setInterpolation( axes.interpolationXY( axes.linearToken, axes.linearToken ) )

        if( cls is None ) : cls = V_W_XYs
        n = cls( axes_ )
        for w_xys in self : n.append( w_xys.toPointwiseLinear( accuracy, lowerEps = lowerEps, upperEps = upperEps ) )
        return( n )

    def toString( self ) :

        lines = []
        for xys in self : lines.append( xys.toString( prefix = "%16.8e" % xys.value ) )
        return( '\n'.join( lines ) )

    def toXML( self, tag = 'xData', indent = '', incrementalIndent = '  ', pairsPerLine = 100, xyFormatter = None, xySeparater = ' ' ) :

        return( '\n'.join( self.toXMLList( indent = indent, incrementalIndent = incrementalIndent, pairsPerLine = pairsPerLine, xyFormatter = xyFormatter, 
            xySeparater = xySeparater ) ) )

    def toXMLList( self, tag = 'xData', indent = '', incrementalIndent = '  ', pairsPerLine = 100, xyFormatter = None, xySeparater = ' ' ) :

        if( hasattr( self, 'tag' ) ) : tag = self.tag
        if( xyFormatter is None ) : xyFormatter = XYFormatter
        indent2 = indent + incrementalIndent
        xmlString = [ '%s<%s xData="%s">' % ( indent, tag, self.xData ) ] 
        xmlString += self.axes.toXMLList( indent = indent2 )
        for w_xys in self.w_xys : xmlString += w_xys.toXMLList( tag = self.axes[0].getLabel( ), indent = indent2, incrementalIndent = incrementalIndent, \
            pairsPerLine = pairsPerLine, xyFormatter = xyFormatter, xySeparater = xySeparater )
        xmlString[-1] += '</%s>' % tag
        return( xmlString )

def XYFormatter( x, y ) :

    return( '%s %s' % ( physicalQuantityWithUncertainty.toShortestString( x ), physicalQuantityWithUncertainty.toShortestString( y ) ) )
