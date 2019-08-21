#! /bin/env python

# <<BEGIN-copyright>>
# <<END-copyright>>

"""
Some simple stuff that should repeat.
"""
import sys
sys.path.append( '../../../lib' )

import random
import pointwiseXY_C

d = pointwiseXY_C.pointwiseXY_C( initialSize = 7, overflowSize = 3 )

xMin, xMax = 1, 100
yMin, yMax = -1., 0.
n = 100000
n_10 = n / 10
random.seed( 314159 )
for i in xrange( n ) :
    if( ( i % n_10 ) == 0 ) : print i
    r = random.random()
    x = xMin * r + xMax * ( 1. - r )
    r = random.random()
    y = yMin * r + yMax * ( 1. - r )
    d.setValue( x, y )

xm = xMin - 1
f = open( "Temp/t6.out", "w" )
status = False
for x, y in d :
    if( x < xm ) : status = True
    f.write( '%.12f %.12f\n' % ( x, y ) )
    xm = x
f.close( )
if( status ) : raise "x < xm"
