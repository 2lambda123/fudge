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

"""
This module contains routines for plotting multiple data sets on the same plot.
"""

import os, types
from fudge.core import fudgemisc
from fudge.core.utilities import fudgeFileMisc, subprocessing
from fudge import __path__
import plotbase


def multiPlot( datasets, xylog = 0, xMin = None, xMax = None, yMin = None, yMax = None, xLabel = "Energy (MeV)",
        yLabel = "Cross section (barn)", title = None, lineWidth = 1, fontSize = None ) :
    """This routine sends all data objects of the first argument, datasets, to the module fudge2dMultiPlot for interactive plotting. 
Here, datasets must be a list or tuple, and each element must be an object at has the method copyDataToXYs. The copyDataToXYs
must return the [x, y] pairs of data to plot as a python list of [x_i,y_i] pairs.  The legend for each data element of datasets 
is taken from that object's label member."

See module fudge2dMultiPlot for a description of the following parameters::
    xylog    xMin     xMax     yMin     
    yMax     xLabel   yLabel   title    

Currently, lineWitdh and fontSize are not implemented.

Examples of usages where d1, d2 and d3 are endl2dmath objects.

>>> d2.label = "Bad data from boss"                     # Sets the legend for d2 to "Bad data from boss".
>>> multiPlot( ( d1, d2, d3 ), xylog = 3 )
>>> I0Data = za.findDatas( I = 0, C = ( 12, 13, 14 ) )  # za is an endlZA object.
>>> multiPlot( I0Data )

Also see the routine qmultiPlot.
"""

    if( len( datasets ) == 0 ) : return
    if( ( type( datasets ) != type( [] ) ) and ( type( datasets ) != type( () ) ) ) : datasets = [ datasets ]
    fs = []
    for dataset in datasets :
        isInstance = ( type( dataset ) == types.InstanceType )
        if( hasattr( dataset, '__class__' ) ) : isInstance |= ( type( dataset ) == dataset.__class__ )    # New style class instance.
        if( isInstance ) :
            Msg = "cannot plot object of type %s" % dataset.__class__.__name__
            try :
                xys = dataset.copyDataToXYs( )
            except :
                print "Warning in multiPlot: cannot plot object named %s" % dataset.__class__.__name__
                continue
            f = fudgeFileMisc.fudgeTempFile( )
            for x, y in xys : f.write( "%.10e %14.8e\n" % ( x, y ) )
            f.close( )
            fs.append( f.getName( ) )
            if( hasattr( dataset, 'label' ) ) :
                if( isinstance( dataset.label, str ) ) : fs += [ 'title', dataset.label ]
        else :
            raise Exception( "\nError in multiPlot: cannot plot none instance object" )

    o = plotbase.parsePlotOptions( xMin, xMax, yMin, yMax, xLabel, yLabel, title )
    p = fudgemisc.findPythonFile( os.sep.join( __path__ + [ "vis", "gnuplot", "fudge2dMultiPlot.py" ] ) )
    s = [ 'python', p, 'xylog', str( xylog ) ] + o + [ 'files' ] + fs
    subprocessing.spawn( s )

def qmultiPlot( dataList, xylog = 0, xMin = None, xMax = None, yMin = None, yMax = None, xLabel = "Energy (MeV)", 
        yLabel = "Cross section (barn)", title = None, legends = [], lineWidth = 1, fontSize = None ) :
    """This routine plots the data objects of the first argument, dataList, to a non-interactive plot.
The argument lineWidth sets the width of the lines and fontSize sets the font size for the plot.
The argument legends is a deprecated argument. To specify a legend for a data set, use that data's
label member.

Examples of usages where d1, d2 and d3 are endl2dmath objects.

>>> d2.label = "Bad data from boss"                     # Sets the legend for d2 to "Bad data from boss".
>>> multiPlot( ( d1, d2, d3 ), xylog = 3 )
>>> I0Data = za.findDatas( I = 0, C = ( 12, 13, 14 ) )  # za is an endlZA object.
>>> multiPlot( I0Data )

See the routine multiPlot for additional information."""

    import Gnuplot
    xylog = int( xylog )            # Allow argument to be a string
    if( xMin is not None ) : xMin = float( xMin )
    if( xMax is not None ) : xMax = float( xMax )
    if( yMin is not None ) : yMin = float( yMin )
    if( yMax is not None ) : yMax = float( yMax )
    lineWidth = float( lineWidth )

    def qmultiPlotAddPlot( dataset, g, t, withLineWidth ) :

        f = fudgeFileMisc.fudgeTempFile( )
        for x, y in dataset.copyDataToXYs( ) : f.write( "%.12e %.12e\n" % ( x, y ) )
        f.close( )
        gf = Gnuplot.File( f.getName( ), title = t ) # , with = withLineWidth )
        gf._options['with'] = ( withLineWidth, 'with ' + withLineWidth )
        g._add_to_queue( [ gf ] )

    if( len( dataList ) == 0 ) : return
    g = Gnuplot.Gnuplot( )
    withLineWidth = 'line linewidth %f' % lineWidth
    nl = len( legends )
    if( ( type( dataList ) != type( [] ) ) and ( type( dataList ) != type( () ) ) ) : dataList = [ dataList ]
    for i1, dataset in enumerate( dataList ) :
        try :
            t = dataset.label
        except :
            t = 'unknown %s' % i1
            if( i1 < nl ) : t = legends[i1]
        isInstance = ( type( dataset ) == types.InstanceType )
        if( hasattr( dataset, '__class__' ) ) : isInstance |= ( type( dataset ) == dataset.__class__ )    # New style class instance.
        if( isInstance ) :
            Msg = "cannot plot object of type %s" % dataset.__class__.__name__
            try :
                xys = dataset.copyDataToXYs( )
                qmultiPlotAddPlot( dataset, g, t, withLineWidth )
            except :
                if( dataset.__class__.__name__ == "endlZA" ) :
                    for F in dateset.filelist :
                        if( F.levels != [] ) and ( F.levels.columns( ) == 2 ) :
                            for i in F.levels : qmultiPlotAddPlot( i, g, t, withLineWidth )
                else :
                    print "Warning in qmultiPlot: cannot plot object named %s" % dateset.__class__.__name__
        else :
            print 'Warning in qmultiPlot: cannot plot object of type "%s"' % type( dateset )
    if( title is None ) : title = "Untitled"
    g( 'set title "' + title + '"' )
    g( 'set style data linespoints' )
    if  ( xylog == 1 ) : g( 'set logscale x' )
    elif( xylog == 2 ) : g( 'set logscale y' )
    elif( xylog == 3 ) : g( 'set logscale xy' )
    if( xMin is not None ) or ( xMax is not None ) :
        if( xMin is None ) :
            s = 'set xrange [ * to %e ]' % xMax
        elif( xMax is None ) :
            s = 'set xrange [ %e to * ]' % xMin
        else :
            s = 'set xrange [ %e to %e ]' % ( xMin, xMax )
        g( s )
    if( yMin is not None ) or ( yMax is not None ) :
        if( yMin is None ) :
            s = 'set yrange [ * to %e ]' %  yMax
        elif( yMax is None ) :
            s = 'set yrange [ %e to * ]' % yMin
        else :
            s = 'set yrange [ %e to %e ]' % ( yMin, yMax )
        g( s )
    if( fontSize is not None ) : g( 'set terminal x11 font "times,%d"' % fontSize )
    g( "set xlabel %s" % `xLabel` )
    g( "set ylabel %s" % `yLabel` )
    g.replot( )
    return g

def multiPlot3d( dataList, xyzlog = 0, xMin = None, xMax = None, yMin = None, yMax = None, zMin = None, zMax = None, xLabel = None,
        yLabel = None, zLabel = None, title = None, lineWidth = 1, fontSize = None ) :
    """
    This routine sends all data objects of the first argument, dataList, to the module fudge3dMultiPlot for interactive plotting.
    Here, dataList must be a list or tuple, and each element must be an endl3dmath object or subclass of it.
    The legend for each data element of dataList is taken from that object's label member."

    See module fudge3dMultiPlot for a description of the following parameters::
        xyzlog   xMin     xMax     yMin     yMax
        zMin     zMax     xLabel   yLabel   zLabel
        title

    Currently, lineWitdh and fontSize are not implemented.

    Examples of usages where d1, d2 and d3 are endl3dmath objects.

    >>> d2.label = "Bad data from boss"                     # Sets the legend for d2 to "Bad data from boss".
    >>> multiPlot3d( ( d1, d2, d3 ), xyzlog = 3 )           # x log, y log and z linear.
    >>> I1Data = za.findDatas( I = 1, C = ( 12, 13, 14 ) )  # za is an endlZA object.
    >>> multiPlot( I1Data )
    """

    def getLabel( self, labelName, labelStr ) :

        if( labelStr is not None ) : return( labelStr )
        if( hasattr( self, labelName ) ) : return( getattr( self, labelName ) )
        return( labelStr )

    if( len( dataList ) == 0 ) : return
    if( not( isinstance( dataList, ( list, tuple ) ) ) ) : dataList = [ dataList ]
    fs = []
    for dataset in dataList :
        w_xys = dataset.copyDataToW_XYs( )
        xLabel = getLabel( dataset, 'xLabel', xLabel )
        yLabel = getLabel( dataset, 'yLabel', yLabel )
        zLabel = getLabel( dataset, 'zLabel', zLabel )
        f = fudgeFileMisc.fudgeTempFile( )
        fs += [ f.getName( ) ]
        if( hasattr( dataset, 'label' ) ) : fs += [ 'title', dataset.label ]
        for x, yz in w_xys :
            xs = "%.10e" % x
            for y, z in yz : f.write( "%s %.10e %14.8e\n" % ( xs, y, z ) )
            f.write( "\n" )
        f.close( )
    o = plotbase.parsePlotOptions( xMin, xMax, yMin, yMax, xLabel, yLabel, title, zMin, zMax, zLabel )
    p = fudgemisc.findPythonFile( os.sep.join( __path__ + [ "vis", "gnuplot", "fudge3dMultiPlot.py" ] ) )
    s = [ 'python', p, 'xyzlog', str( xyzlog ) ] + o + [ 'files' ] + fs
    subprocessing.spawn( s )
