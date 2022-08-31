#! /usr/bin/env python3

# <<BEGIN-copyright>>
# Copyright 2022, Lawrence Livermore National Security, LLC.
# See the top-level COPYRIGHT file for details.
# 
# SPDX-License-Identifier: BSD-3-Clause
# <<END-copyright>>

import random

from PoPs import database as databaseModule
from PoPs import alias as aliasModule

from PoPs.chemicalElements import misc as chemicalElementMiscModule

from PoPs.quantities import quantity as quantityModule
from PoPs.quantities import mass as massModule
from PoPs.quantities import spin as spinModule
from PoPs.quantities import parity as parityModule
from PoPs.quantities import charge as chargeModule
from PoPs.quantities import halflife as halflifeModule
from PoPs.quantities import nuclearEnergyLevel as nuclearEnergyLevelModule

from PoPs.families import gaugeBoson as gaugeBosonModule
from PoPs.families import lepton as leptonModule
from PoPs.families import baryon as baryonModule
from PoPs.families import nuclide as nuclideModule

database = databaseModule.Database( 'test', '1.2.3' )

def nuclides( Z, A, data ) :

    symbol = chemicalElementMiscModule.symbolFromZ[Z]
    isotopeID = chemicalElementMiscModule.isotopeSymbolFromChemicalElementIDAndA( symbol, A )
    keys = random.sample( [ key for key in data ], len( data ) )
    for index in keys :
        mass, energy, charge, halflife, spin, parity = data[index]

        name = chemicalElementMiscModule.nuclideIDFromIsotopeSymbolAndIndex( isotopeID, index )
        level = nuclideModule.Particle( name )
        energy = nuclearEnergyLevelModule.Double( 'base', energy, quantityModule.stringToPhysicalUnit( 'keV' ) )
        level.nucleus.energy.add( energy )

        if( mass is not None ) :
            mass = massModule.Double( 'base', mass, quantityModule.stringToPhysicalUnit( 'amu' ) )
            level.mass.add( mass )

        if( charge is not None ) :
            charge = chargeModule.Integer( 'base', charge, quantityModule.stringToPhysicalUnit( 'e' ) )
            level.charge.add( charge )

        if( halflife is not None ) :
            time, unit = halflife.split( )
            halflife = halflifeModule.Double( 'base', float( time ), quantityModule.stringToPhysicalUnit( unit ) )
            level.halflife.add( halflife )

        if( spin is not None ) :
            spin = spinModule.Fraction( 'base', spinModule.Fraction.toValueType( spin ), quantityModule.stringToPhysicalUnit( 'hbar' ) )
            level.spin.add( spin )

        if( parity is not None ) :
            parity = parityModule.Integer( 'base', parity, quantityModule.stringToPhysicalUnit( '' ) )
            level.parity.add( parity )

        database.add( level )

#                             mass,  energy, charge, halflife, spin, parity
O16Data = { 0 : [ 15.99491461956,       0,   None,     None, None,   None ],
            1 : [           None, 6049.400,   None,     None, None,   None ],
            2 : [           None, 6129.893,   None,     None, None,   None ],
            3 : [           None, 6917.100,   None,     None, None,   None ] }
for A, data in [ [ 17, O16Data ], [ 16, O16Data ] ] : nuclides( 8, A, data )

#                             mass,  energy, charge,  halflife, spin, parity
Am242Data = { 0 : [ 242.059549159,      0,   None, '16.02 h',    1,     -1 ],
              1 : [          None, 44.092,   None,      None,    0,     -1 ],
              2 : [          None,  48.60,   None,  '141 yr',    5,     -1 ],
              3 : [          None,  52.70,   None,      None,    3,     -1 ] }
nuclides( 95, 242, Am242Data )
database.add(aliasModule.MetaStable('Am242_m1', 'Am242_e2', 1))

photon = gaugeBosonModule.Particle( 'photon' )

mass = massModule.Double( 'base', 0, quantityModule.stringToPhysicalUnit( 'amu' ) )
photon.mass.add( mass )

charge = chargeModule.Integer( 'base', 0, quantityModule.stringToPhysicalUnit( 'e' ) )
photon.charge.add( charge )

halflife = halflifeModule.String( 'base', 'stable', quantityModule.stringToPhysicalUnit( 's' ) )
photon.halflife.add( halflife )

spin = spinModule.Fraction( 'base', spinModule.Fraction.toValueType( '1' ), quantityModule.stringToPhysicalUnit( 'hbar' ) )
photon.spin.add( spin )

parity = parityModule.Integer( 'base', 1, quantityModule.stringToPhysicalUnit( '' ) )
photon.parity.add( parity )

database.add( photon )

leptons = [ [ 'e-',      5.48579909070e-4, -1,     'stable', '1/2',  1, 'electronic' ],
            [ 'e-_anti', 5.48579909070e-4,  1,     'stable', '1/2', -1, 'electronic' ],
            [ 'mu',      0.1134289267,     -1, 2.1969811e-6, '1/2',  1, 'muonic' ] ]

for id, mass, charge, halflife, spin, parity, generation in leptons :
    lepton = leptonModule.Particle( id, generation = generation )

    mass = massModule.Double( 'base', mass, quantityModule.stringToPhysicalUnit( 'amu' ) )
    lepton.mass.add( mass )

    charge = chargeModule.Integer( 'base', charge, quantityModule.stringToPhysicalUnit( 'e' ) )
    lepton.charge.add( charge )

    if( halflife == 'stable' ) :
        halflife = halflifeModule.String( 'base', halflife, quantityModule.stringToPhysicalUnit( 's' ) )
    else :
        halflife = halflifeModule.Double( 'base', halflife, quantityModule.stringToPhysicalUnit( 's' ) )
    lepton.halflife.add( halflife )

    spin = spinModule.Fraction( 'base', spinModule.Fraction.toValueType( spin ), quantityModule.stringToPhysicalUnit( 'hbar' ) )
    lepton.spin.add( spin )

    parity = parityModule.Integer( 'base', parity, quantityModule.stringToPhysicalUnit( '' ) )
    lepton.parity.add( parity )

    database.add( lepton )

database.add(aliasModule.Alias('electron', 'e-'))
database.add(aliasModule.Alias('e+', 'e-_anti'))
database.add(aliasModule.Alias('positron', 'e-_anti'))

baryons = [ [ 'n', 1.00866491588,     0,    881.5, '1/2', 1 ],
            [ 'p', 1.007276466812,    1, 'stable', '1/2', 1 ] ]

for _id, _mass, _charge, _halflife, _spin, _parity in baryons :
    for anti in [ '', '_anti' ] :
        baryon = baryonModule.Particle( _id + anti )

        mass = massModule.Double( 'base', _mass, quantityModule.stringToPhysicalUnit( 'amu' ) )
        baryon.mass.add( mass )

        charge = chargeModule.Integer( 'base', _charge, quantityModule.stringToPhysicalUnit( 'e' ) )
        baryon.charge.add( charge )

        if( _halflife == 'stable' ) :
            halflife = halflifeModule.String( 'base', _halflife, quantityModule.stringToPhysicalUnit( 's' ) )
        else :
            halflife = halflifeModule.Double( 'base', _halflife, quantityModule.stringToPhysicalUnit( 's' ) )
        baryon.halflife.add( halflife )

        spin = spinModule.Fraction( 'base', spinModule.Fraction.toValueType( _spin ), quantityModule.stringToPhysicalUnit( 'hbar' ) )
        baryon.spin.add( spin )

        parity = parityModule.Integer( 'base', _parity, quantityModule.stringToPhysicalUnit( '' ) )
        baryon.parity.add( parity )

        database.add( baryon )

xmld1 = database.toXML( )
print( xmld1 )
database2 = database.parseXMLString(xmld1)
if( xmld1 != database2.toXML( ) ) : raise Exception( 'Fix me.' )
