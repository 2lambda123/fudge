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
*/

/*
    This routine tests the not mutual domain logic. It multiplies or divides two ptwXYPoints (u and v) and checks the return status 
    for the following cases.
      Multiplication tests.
        1) Domain of u greater than that of v at both ends and end points of v contain non-zero y-values.
        2) Same as test 1 except lower v point has zero y-value.
        3) Same as test 1 except upper v point has zero y-value.
        4) Same as test 1 except lower and upper v points have zero y-values.
      Division tests with same domain as 4.
        5) v / u, no safe divide should fail with nfu_divByZero
        6) v / u, safe divide should pass.
        7) u / v, safe divide should fail with nfu_XOutsideDomain.
        8) v / u, same as 6 execpt lower v point has non-zero y-value.
*/
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <math.h>
#include <stdarg.h>

#include <ptwXY.h>

static int verbose = 0;

void printMsg( char const *fmt, ... );
/*
****************************************************************
*/
int main( int argc, char **argv ) {

    int Test, iarg, echo = 0;
    ptwXYPoints *u, *v, *m;
    double uXY[] = { 1.0, 11.0, 2.66, 1.7, 3.14, 3.12, 3.66, -1.6, 7.66, 1.5 };
    double vXY[] = { 3.732, 1.760, 5.598, 4.349, 5.679, 7.934, 6.459, 4.288, 6.557, 6.787, 6.838, -0.92423, 7.1138, 6.5695 };
    int nuXY = sizeof( uXY ) / ( 2 * sizeof( double ) ), nvXY = sizeof( vXY ) / ( 2 * sizeof( double ) );
    nfu_status status;
    FILE *ff;
    char *fmt = "%10.5f %12.5f\n";

    nfu_setMemoryDebugMode( 0 );

    for( iarg = 1; iarg < argc; iarg++ ) {
        if( strcmp( "-v", argv[iarg] ) == 0 ) {
            verbose = 1; }
        else if( strcmp( "-e", argv[iarg] ) == 0 ) {
            echo = 1; }
        else {
            printMsg( "Error %s: unsupported option = '%s'", __FILE__, argv[iarg] );
        }
    }
    if( echo ) printf( "%s\n", __FILE__ );


    if( ( u = ptwXY_create( ptwXY_interpolationLinLin, NULL, 3, 1e-3, 10, 10, nuXY, uXY, &status, 0 ) ) == NULL ) printMsg( "u creation: status = %d: %s", 
        status, nfu_statusMessage( status ) );
    if( ( v = ptwXY_create( ptwXY_interpolationLinLin, NULL, 3, 1e-3, 10, 10, nvXY, vXY, &status, 0 ) ) == NULL ) printMsg( "v creation: status = %d: %s", 
        status, nfu_statusMessage( status ) );

    ff = fopen( "curve_u.dat", "w" );
    ptwXY_simpleWrite( u, ff, fmt );
    if( verbose ) ptwXY_simpleWrite( u, stdout, fmt );
    if( verbose ) printf( "\n" );
    fclose( ff );

    ff = fopen( "curve_v.dat", "w" );
    ptwXY_simpleWrite( v, ff, fmt );
    if( verbose ) ptwXY_simpleWrite( v, stdout, fmt );
    if( verbose ) printf( "\n" );
    fclose( ff );

    ff = fopen( "curve_o.dat", "w" );

Test = 1;                               /* This must produce a nfu_domainsNotMutual error. */
    if( ( m = ptwXY_mul2_ptwXY( u, v, &status ) ) == NULL ) {
        if( status != nfu_domainsNotMutual ) printMsg( "Test %d multiplication: status = %d: %s", Test, status, nfu_statusMessage( status ) ); }
    else {
        printMsg( "Test %d multiplication: should have failed with '%s'", Test, nfu_statusMessage( nfu_domainsNotMutual ) );
        ptwXY_free( m );
    }

Test = 2;                               /* This must produce a nfu_domainsNotMutual error. */
    ptwXY_setValueAtX( v, vXY[0], 0. );
    if( verbose ) ptwXY_simpleWrite( v, stdout, fmt );
    if( verbose ) printf( "\n" );
    if( ( m = ptwXY_mul2_ptwXY( u, v, &status ) ) == NULL ) {
        if( status != nfu_domainsNotMutual ) printMsg( "Test %d multiplication: status = %d: %s", Test, status, nfu_statusMessage( status ) ); }
    else {
        printMsg( "Test %d multiplication: should have failed with: %s", Test, nfu_statusMessage( nfu_domainsNotMutual ) );
        ptwXY_free( m );
    }

Test = 3;                               /* This must produce a nfu_domainsNotMutual error. */
    ptwXY_setValueAtX( v, vXY[0], 1. );
    ptwXY_setValueAtX( v, vXY[2 * ( nvXY - 1 )], 0. );
    if( verbose ) ptwXY_simpleWrite( v, stdout, fmt );
    if( verbose ) printf( "\n" );
    if( ( m = ptwXY_mul2_ptwXY( u, v, &status ) ) == NULL ) {
        if( status != nfu_domainsNotMutual ) printMsg( "Test %d multiplication: status = %d: %s", Test, status, nfu_statusMessage( status ) ); }
    else {
        printMsg( "Test %d multiplication: should have failed with: %s", Test, nfu_statusMessage( nfu_domainsNotMutual ) );
        ptwXY_free( m );
    }

Test = 4;                               /* This must work. */
    ptwXY_setValueAtX( v, vXY[0], 0. );
    if( verbose ) ptwXY_simpleWrite( v, stdout, fmt );
    if( verbose ) printf( "\n" );
    if( ( m = ptwXY_mul2_ptwXY( u, v, &status ) ) == NULL ) {
        printMsg( "Test %d multiplication: status = %d: %s", Test, status, nfu_statusMessage( status ) ); }
    else {
        ptwXY_simpleWrite( m, ff, fmt );
        fprintf( ff, "\n" );
        if( verbose ) ptwXY_simpleWrite( m, stdout, fmt );
        if( verbose ) printf( "\n" );
        ptwXY_free( m );
    }

Test = 5;                               /* This must cause a nfu_divByZero error. */
    if( ( m = ptwXY_div_ptwXY( v, u, &status, 0 ) ) == NULL ) {
        if( status != nfu_divByZero ) printMsg( "Test %d division: status = %d: %s", Test, status, nfu_statusMessage( status ) ); }
    else {
        printMsg( "Test %d division: should have failed with: %s", Test, nfu_statusMessage( nfu_divByZero ) );
        ptwXY_free( m );
    }

Test = 6;                               /* This must work. */
    if( ( m = ptwXY_div_ptwXY( v, u, &status, 1 ) ) == NULL ) {
        printMsg( "Test %d division: status = %d: %s", Test, status, nfu_statusMessage( status ) ); }
    else {
        ptwXY_simpleWrite( m, ff, fmt );
        fprintf( ff, "\n" );
        if( verbose ) ptwXY_simpleWrite( m, stdout, fmt );
        if( verbose ) printf( "\n" );
        ptwXY_free( m );
    }

Test = 7;                               /* This must cause a nfu_XOutsideDomain error. */
    if( ( m = ptwXY_div_ptwXY( u, v, &status, 1 ) ) == NULL ) {
        if( status != nfu_XOutsideDomain ) printMsg( "Test %d division: status = %d: %s", Test, status, nfu_statusMessage( status ) ); }
    else {
        printMsg( "Test %d division: should have failed with: %s", Test, nfu_statusMessage( nfu_XOutsideDomain ) );
        ptwXY_free( m );
    }

Test = 8;                               /* This must cause a nfu_domainsNotMutual error. */
    ptwXY_setValueAtX( v, vXY[0], 1. );
    if( ( m = ptwXY_div_ptwXY( v, u, &status, 1 ) ) == NULL ) {
        if( status != nfu_domainsNotMutual ) printMsg( "Test %d division: status = %d: %s", Test, status, nfu_statusMessage( status ) ); }
    else {
        printMsg( "Test %d division: should have failed with: %s", Test, nfu_statusMessage( nfu_domainsNotMutual ) );
        ptwXY_free( m );
    }

    fclose( ff );
    ptwXY_free( u );
    ptwXY_free( v );

    exit( EXIT_SUCCESS );
}
/*
****************************************************************
*/
void printMsg( char const *fmt, ... ) {

    va_list args;

    va_start( args, fmt );
    vfprintf( stderr, fmt, args );
    fprintf( stderr, "\n" );
    va_end( args );
    exit( EXIT_FAILURE );
}
