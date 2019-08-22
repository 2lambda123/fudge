/*
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
*/

#include <stdio.h>
#include <stdlib.h>
#include <nf_specialFunctions.h>

struct aFOfA {
    double a, f;
};

#include "gammaTest.dat"

#define nPowerErrors 10
static int verbose = 0;

/*
************************************************************
*/
int main( int argc, char **argv ) {

    int i1, i2, nData = sizeof( data ) / sizeof( data[0] ), counts = 0, iarg, echo = 0, powerErrors[nPowerErrors+1], info = 0;
    double f, r, r2;
    nfu_status status;

    for( iarg = 1; iarg < argc; iarg++ ) {
        if( strcmp( "-v", argv[iarg] ) == 0 ) {
            verbose = 1; }
        else if( strcmp( "-e", argv[iarg] ) == 0 ) {
            echo = 1; }
        else if( strcmp( "-i", argv[iarg] ) == 0 ) {
            info = 1; }
        else {
            nfu_printErrorMsg( "ERROR %s: invalid input option '%s'", __FILE__, argv[iarg] );
        }
    }
    if( echo ) printf( "%s\n", __FILE__ );

    for( i2 = 0; i2 <= nPowerErrors; i2++ ) powerErrors[i2] = 0;

    for( i1 = 0; i1 < nData; i1++ ) {
        f = nf_gammaFunction( data[i1].a, &status );
        r = 1;
        if( data[i1].f != 0. ) {
            r = f / data[i1].f - 1; }
        else {
            if( f == 0. ) r = 0.;
        }
        if( ( fabs( r ) > 3e-15 ) || status ) {
            printf( "%.17e %.17e %.17e %+.3e  %d\n", data[i1].a, data[i1].f, f, r, status );
            counts++;
        }
        for( i2 = 0, r2 = 1e-16; i2 < nPowerErrors; i2++, r2 *= 10. ) {
            if( fabs( r ) < r2 ) break;
        }
        powerErrors[i2]++;
    }
    if( info ) {
        printf( "relative" );
        for( i2 = 0; i2 <= nPowerErrors; i2++ ) printf( " %7d", -i2 - 6 );
        printf( "\n" );
        printf( "error:  " );
        for( i2 = 0; i2 <= nPowerErrors; i2++ ) printf( "%s%5d  %s", ( ( i2 < 4 ) ? " " : "" ), 10, ( ( i2 >= 4 ) ? " " : "" ) );
        printf( "\n" );

        printf( "--------" );
        for( i2 = 0; i2 <= nPowerErrors; i2++ ) printf( "--------" );
        printf( "\n" );

        printf( "counts: " );
        for( i2 = nPowerErrors; i2 >= 0; i2-- ) printf( " %7d", powerErrors[i2] );
        printf( "\n" );
    }
    exit( counts );
}
