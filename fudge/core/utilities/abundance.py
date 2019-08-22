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

'''
Directory: masses/
File:      abundance.readme (December 10, 2007)
***********************************************

			    abundance.dat

		Natural abundances of stable isotopes
	      (provided by M. Herman, December 10, 2007)
              ******************************************


Content
-------
The abundance file is a reformatted version of the file from the
Nuclear Wallet cards (2005), as retrieved from Brookhaven National
Laboratory. The abundances are given for all stable isotopes.


Format
------
Each record of the file contains: 

   Z        : charge number
   A        : mass number
   El       : element symbol
   abundance: abundance in %
   uncert   : uncertainties in abundance in %

The corresponding FORTRAN format is (2i4,1x,a2,1x,2f10.6)

References
----------
[1] J.K. Tuli, Nuclear Wallet Cards (NNDC, Brookhaven National Laboratory), 2005.

Dates: Original 10 December, 2007
'''

__data = '''
#      Natural abundances
#  Z  A  El   abundance  uncert.
#               [%]       [%]
#-------------------------------
   1   1 H   99.985001  0.001000
   1   2 H    0.015000  0.001000
   2   3 He   0.000137  0.000003
   2   4 He  99.999863  0.000003
   3   6 Li   7.590000  0.040000
   3   7 Li  92.410004  0.040000
   4   9 Be 100.000000  0.000000
   5  10 B   19.799999  0.300000
   5  11 B   80.199997  0.300000
   6  12 C   98.889999  0.010000
   6  13 C    1.110000  0.010000
   7  14 N   99.634003  0.020000
   7  15 N    0.366000  0.020000
   8  16 O   99.762001  0.016000
   8  17 O    0.038000  0.001000
   8  18 O    0.200000  0.014000
   9  19 F  100.000000  0.000000
  10  20 Ne  90.480003  0.030000
  10  21 Ne   0.270000  0.010000
  10  22 Ne   9.250000  0.030000
  11  23 Na 100.000000  0.000000
  12  24 Mg  78.989998  0.040000
  12  25 Mg  10.000000  0.010000
  12  26 Mg  11.010000  0.030000
  13  27 Al 100.000000  0.000000
  14  28 Si  92.230003  0.019000
  14  29 Si   4.683000  0.008000
  14  30 Si   3.087000  0.005000
  15  31 P  100.000000  0.000000
  16  32 S   95.019997  0.090000
  16  33 S    0.750000  0.010000
  16  34 S    4.210000  0.080000
  16  36 S    0.020000  0.010000
  17  35 Cl  75.769997  0.040000
  17  37 Cl  24.230000  0.040000
  18  36 Ar   0.336500  0.003000
  18  38 Ar   0.063200  0.000500
  18  40 Ar  99.600304  0.003000
  19  39 K   93.258102  0.004400
  19  40 K    0.011700  0.000100
  19  41 K    6.730200  0.004400
  20  40 Ca  96.940002  0.160000
  20  42 Ca   0.647000  0.023000
  20  43 Ca   0.135000  0.010000
  20  44 Ca   2.090000  0.110000
  20  46 Ca   0.004000  0.003000
  20  48 Ca   0.187000  0.021000
  21  45 Sc 100.000000  0.000000
  22  46 Ti   8.250000  0.030000
  22  47 Ti   7.440000  0.020000
  22  48 Ti  73.720001  0.030000
  22  49 Ti   5.410000  0.020000
  22  50 Ti   5.180000  0.020000
  23  50 V    0.250000  0.002000
  23  51 V   99.750000  0.002000
  24  50 Cr   4.345000  0.013000
  24  52 Cr  83.789001  0.018000
  24  53 Cr   9.501000  0.017000
  24  54 Cr   2.365000  0.007000
  25  55 Mn 100.000000  0.000000
  26  54 Fe   5.845000  0.035000
  26  56 Fe  91.753998  0.036000
  26  57 Fe   2.119000  0.010000
  26  58 Fe   0.282000  0.004000
  27  59 Co 100.000000  0.000000
  28  58 Ni  68.077003  0.009000
  28  60 Ni  26.223000  0.008000
  28  61 Ni   1.140000  0.001000
  28  62 Ni   3.634000  0.002000
  28  64 Ni   0.926000  0.001000
  29  63 Cu  69.169998  0.030000
  29  65 Cu  30.830000  0.030000
  30  64 Zn  48.630001  0.600000
  30  66 Zn  27.900000  0.270000
  30  67 Zn   4.100000  0.130000
  30  68 Zn  18.750000  0.510000
  30  70 Zn   0.620000  0.030000
  31  69 Ga  60.108002  0.009000
  31  71 Ga  39.891998  0.009000
  32  70 Ge  20.370001  0.180000
  32  72 Ge  27.309999  0.260000
  32  73 Ge   7.760000  0.080000
  32  74 Ge  36.730000  0.150000
  32  76 Ge   7.830000  0.070000
  33  75 As 100.000000  0.000000
  34  74 Se   0.890000  0.040000
  34  76 Se   9.370000  0.290000
  34  77 Se   7.630000  0.160000
  34  78 Se  23.770000  0.280000
  34  80 Se  49.610001  0.410000
  34  82 Se   8.730000  0.220000
  35  79 Br  50.689999  0.070000
  35  81 Br  49.310001  0.070000
  36  78 Kr   0.350000  0.010000
  36  80 Kr   2.280000  0.060000
  36  82 Kr  11.580000  0.140000
  36  83 Kr  11.490000  0.060000
  36  84 Kr  57.000000  0.040000
  36  86 Kr  17.299999  0.220000
  37  85 Rb  72.169998  0.020000
  37  87 Rb  27.830000  0.020000
  38  84 Sr   0.560000  0.010000
  38  86 Sr   9.860000  0.010000
  38  87 Sr   7.000000  0.010000
  38  88 Sr  82.580002  0.010000
  39  89 Y  100.000000  0.000000
  40  90 Zr  51.450001  0.400000
  40  91 Zr  11.220000  0.050000
  40  92 Zr  17.150000  0.080000
  40  94 Zr  17.379999  0.280000
  40  96 Zr   2.800000  0.090000
  41  93 Nb 100.000000  0.000000
  42  92 Mo  14.840000  0.350000
  42  94 Mo   9.250000  0.120000
  42  95 Mo  15.920000  0.130000
  42  96 Mo  16.680000  0.020000
  42  97 Mo   9.550000  0.080000
  42  98 Mo  24.129999  0.310000
  42 100 Mo   9.630000  0.230000
  44  96 Ru   5.540000  0.140000
  44  98 Ru   1.870000  0.030000
  44  99 Ru  12.760000  0.140000
  44 100 Ru  12.600000  0.070000
  44 101 Ru  17.059999  0.020000
  44 102 Ru  31.549999  0.140000
  44 104 Ru  18.620001  0.270000
  45 103 Rh 100.000000  0.000000
  46 102 Pd   1.020000  0.010000
  46 104 Pd  11.140000  0.080000
  46 105 Pd  22.330000  0.080000
  46 106 Pd  27.330000  0.030000
  46 108 Pd  26.459999  0.090000
  46 110 Pd  11.720000  0.090000
  47 107 Ag  51.839001  0.008000
  47 109 Ag  48.160999  0.008000
  48 106 Cd   1.250000  0.060000
  48 108 Cd   0.890000  0.030000
  48 110 Cd  12.490000  0.180000
  48 111 Cd  12.800000  0.120000
  48 112 Cd  24.129999  0.210000
  48 113 Cd  12.220000  0.120000
  48 114 Cd  28.730000  0.420000
  48 116 Cd   7.490000  0.180000
  49 113 In   4.290000  0.050000
  49 115 In  95.709999  0.050000
  50 112 Sn   0.970000  0.010000
  50 114 Sn   0.660000  0.010000
  50 115 Sn   0.340000  0.010000
  50 116 Sn  14.540000  0.090000
  50 117 Sn   7.680000  0.070000
  50 118 Sn  24.219999  0.090000
  50 119 Sn   8.590000  0.040000
  50 120 Sn  32.580002  0.090000
  50 122 Sn   4.630000  0.030000
  50 124 Sn   5.790000  0.050000
  51 121 Sb  57.209999  0.050000
  51 123 Sb  42.790001  0.050000
  52 120 Te   0.090000  0.010000
  52 122 Te   2.550000  0.120000
  52 123 Te   0.890000  0.030000
  52 124 Te   4.740000  0.140000
  52 125 Te   7.070000  0.150000
  52 126 Te  18.840000  0.250000
  52 128 Te  31.740000  0.080000
  52 130 Te  34.080002  0.620000
  53 127 I  100.000000  0.000000
  54 124 Xe   0.095000  0.003000
  54 126 Xe   0.089000  0.001000
  54 128 Xe   1.910000  0.022000
  54 129 Xe  26.400000  0.180000
  54 130 Xe   4.071000  0.053000
  54 131 Xe  21.232000  0.062000
  54 132 Xe  26.909000  0.068000
  54 134 Xe  10.436000  0.029000
  54 136 Xe   8.857000  0.033000
  55 133 Cs 100.000000  0.000000
  56 130 Ba   0.106000  0.001000
  56 132 Ba   0.101000  0.001000
  56 134 Ba   2.417000  0.018000
  56 135 Ba   6.592000  0.012000
  56 136 Ba   7.854000  0.024000
  56 137 Ba  11.232000  0.024000
  56 138 Ba  71.697998  0.042000
  57 138 La   0.090000  0.001000
  57 139 La  99.910004  0.001000
  58 136 Ce   0.185000  0.002000
  58 138 Ce   0.251000  0.002000
  58 140 Ce  88.449997  0.018000
  58 142 Ce  11.114000  0.017000
  59 141 Pr 100.000000  0.000000
  60 142 Nd  27.200001  0.500000
  60 143 Nd  12.200000  0.200000
  60 144 Nd  23.799999  0.300000
  60 145 Nd   8.300000  0.100000
  60 146 Nd  17.200001  0.300000
  60 148 Nd   5.700000  0.100000
  60 150 Nd   5.600000  0.200000
  62 144 Sm   3.070000  0.070000
  62 147 Sm  14.990000  0.180000
  62 148 Sm  11.240000  0.100000
  62 149 Sm  13.820000  0.070000
  62 150 Sm   7.380000  0.010000
  62 152 Sm  26.750000  0.160000
  62 154 Sm  22.750000  0.290000
  63 151 Eu  47.810001  0.030000
  63 153 Eu  52.189999  0.030000
  64 152 Gd   0.200000  0.010000
  64 154 Gd   2.180000  0.030000
  64 155 Gd  14.800000  0.120000
  64 156 Gd  20.469999  0.090000
  64 157 Gd  15.650000  0.020000
  64 158 Gd  24.840000  0.070000
  64 160 Gd  21.860001  0.190000
  65 159 Tb 100.000000  0.000000
  66 156 Dy   0.060000  0.010000
  66 158 Dy   0.100000  0.010000
  66 160 Dy   2.340000  0.080000
  66 161 Dy  18.910000  0.240000
  66 162 Dy  25.510000  0.260000
  66 163 Dy  24.900000  0.160000
  66 164 Dy  28.180000  0.370000
  67 165 Ho 100.000000  0.000000
  68 162 Er   0.139000  0.005000
  68 164 Er   1.601000  0.003000
  68 166 Er  33.502998  0.036000
  68 167 Er  22.868999  0.009000
  68 168 Er  26.978001  0.018000
  68 170 Er  14.910000  0.036000
  69 169 Tm 100.000000  0.000000
  70 168 Yb   0.130000  0.010000
  70 170 Yb   3.040000  0.150000
  70 171 Yb  14.280000  0.570000
  70 172 Yb  21.830000  0.670000
  70 173 Yb  16.129999  0.270000
  70 174 Yb  31.830000  0.920000
  70 176 Yb  12.760000  0.410000
  71 175 Lu  97.410004  0.020000
  71 176 Lu   2.590000  0.020000
  72 174 Hf   0.160000  0.010000
  72 176 Hf   5.260000  0.070000
  72 177 Hf  18.600000  0.090000
  72 178 Hf  27.280001  0.070000
  72 179 Hf  13.620000  0.020000
  72 180 Hf  35.080002  0.160000
  73 180 Ta   0.012000  0.002000
  73 181 Ta  99.987999  0.002000
  74 180 W    0.120000  0.010000
  74 182 W   26.500000  0.160000
  74 183 W   14.310000  0.040000
  74 184 W   30.639999  0.020000
  74 186 W   28.430000  0.190000
  75 185 Re  37.400002  0.020000
  75 187 Re  62.599998  0.020000
  76 184 Os   0.020000  0.010000
  76 186 Os   1.590000  0.030000
  76 187 Os   1.600000  0.300000
  76 188 Os  13.290000  0.080000
  76 189 Os  16.209999  0.050000
  76 190 Os  26.360001  0.020000
  76 192 Os  40.930000  0.190000
  77 191 Ir  37.299999  0.200000
  77 193 Ir  62.700001  0.200000
  78 190 Pt   0.014000  0.001000
  78 192 Pt   0.782000  0.007000
  78 194 Pt  32.966999  0.099000
  78 195 Pt  33.832001  0.010000
  78 196 Pt  25.242001  0.041000
  78 198 Pt   7.163000  0.055000
  79 197 Au 100.000000  0.000000
  80 196 Hg   0.150000  0.010000
  80 198 Hg   9.970000  0.200000
  80 199 Hg  16.870001  0.220000
  80 200 Hg  23.100000  0.190000
  80 201 Hg  13.180000  0.090000
  80 202 Hg  29.860001  0.260000
  80 204 Hg   6.870000  0.150000
  81 203 Tl  29.524000  0.014000
  81 205 Tl  70.475998  0.014000
  82 204 Pb   1.400000  0.100000
  82 206 Pb  24.100000  0.100000
  82 207 Pb  22.100000  0.100000
  82 208 Pb  52.400002  0.100000
  83 209 Bi 100.000000  0.000000
  90 232 Th 100.000000  0.000000
  92 234 U    0.005400  0.000500
  92 235 U    0.720400  0.000600
  92 238 U   99.274200  0.001000
  '''
  
def __getAbundanceTuple( line ) :

    sline = line.split()
    Z = int( sline[0] )
    A = int( sline[1] )
    abund = float( sline[3] )
    dAbund = float( sline[4] )
    return ( ( Z, A ), ( abund, dAbund ) )
  
abundances = dict( [ __getAbundanceTuple( __line ) for __line in __data.split('\n')[5:-1] ] )

SymbolToZ = {}
for line in __data.split('\n')[5:-1] :
    sline = line.split()
    Z = int( sline[0] )
    SymbolToZ[Z] = Z
    SymbolToZ[sline[2]] = Z

def getAbundance( Z, A ):

    return abundances.get( ( SymbolToZ.get( Z, Z ), A ), ( 0.0, 0.0 ) )

def getElementsNaturalIsotopes( Z ) :

    Z_, A_abundances = SymbolToZ[Z], {}
    for Z, A in abundances :
        if( Z == Z_ ) : A_abundances[A] = getAbundance( Z, A )
    return( A_abundances )
  
if __name__ == "__main__":

    print getAbundance(1,2)
    print getAbundance('H',2)
    print getAbundance(92,238)
    print getAbundance('U',238)
    print getAbundance(94,239)
    print getAbundance('Pu',239)

    def naturalIsotopes( Z ) :
        __abundances = getElementsNaturalIsotopes( Z )
        print 'Isotopes and abundances for element %s:' % Z
        for A in __abundances : print '   ', A, __abundances[A]

    naturalIsotopes( 'O' )
    naturalIsotopes(   8 )
