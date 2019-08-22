#! /bin/env python

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

import sys
sys.path.insert( 0, '../../../../../lib' )

import listOfDoubles_C
import os, random

if( 'CHECKOPTIONS' in os.environ ) :
    options = os.environ['CHECKOPTIONS'].split( )
    if( '-e' in options ) : print __file__

def compareLists( Msg, list1, list2, CList ) :

    CList2 = [ item for item in CList ]
    Pylist = list1 + list2
    if( Pylist != CList2 ) :
        print len( list1 ), len( list2 )
        print list1
        print list2
        print Pylist
        print CList.toString( format = "%.0f", valuesPerLine = 25, valueSeparator = ', ' )
        print CList2
        raise Exception( 'List differ for %s' % Msg )

def check( list1, list2 ) :

    CList1 = listOfDoubles_C.listOfDoubles_C( list1 )
    CList2 = listOfDoubles_C.listOfDoubles_C( list2 )
    compareLists( 'CList1 + list1',  list1, list1, CList1 + list1 )
    compareLists( 'CList1 + CList1', list1, list1, CList1 + CList1 )
    compareLists( 'CList1 + list2',  list1, list2, CList1 + list2 )
    compareLists( 'CList1 + CList2', list1, list2, CList1 + CList2 )
    compareLists( 'CList2 + list1',  list2, list1, CList2 + list1 )
    compareLists( 'CList2 + CList1', list2, list1, CList2 + CList1 )
    compareLists( 'CList2 + list2',  list2, list2, CList2 + list2 )
    compareLists( 'CList2 + CList2', list2, list2, CList2 + CList2 )
    CList1 += list1
    compareLists( 'CList1 += list1',  list1, list1, CList1 )

values1 = xrange( -3, 5 )
values2 = xrange( -30, 5000 )
for i1 in xrange( 30 ) :
    check( [ float( random.choice( values1 ) ) for j1 in xrange( random.choice( values1 ) ) ], [ float( random.choice( values1 ) ) for j1 in xrange( random.choice( values1 ) ) ] )
    check( [ float( random.choice( values2 ) ) for j1 in xrange( random.choice( values2 ) ) ], [ float( random.choice( values2 ) ) for j1 in xrange( random.choice( values2 ) ) ] )
