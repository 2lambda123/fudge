import numpy

from xData import table as tableModule
from xData import XYs as XYs1dModule

from . import level_generator

def getFakeResonanceSet(
        E0,
        aveD=None,
        numLevels=None,
        style='wigner',
        BrodyW=0.5,
        L=0, J=0,
        levelDensity=None,
        aveWidthFuncs=None,
        DOFs=None,
        widthKeys=('totalWidth', 'neutronWidth', 'captureWidth', 'fissionWidthA', 'competitiveWidth'),
        domainMin=None,
        domainMax=None,
        seed=None,
        verbose=False):

    if seed is not None:
        numpy.random.seed(seed)

    # FIXME assumes levelDensity is not None...
    energyUnit = levelDensity.axes[-1].unit

    DOTIMING = verbose
    if DOTIMING:
        import datetime
        lastTime = datetime.datetime.now()

    if aveWidthFuncs is None:
        aveWidthFuncs = {}

    if DOFs is None:
        DOFs = {}

    # GOE style is fancy and absolutely needs a levelDensity to work
    # FIXME remove this and require evaluator to supply level density? GNDS already requires it...
    if levelDensity is None and style == "goe":
        if domainMax is not None and E0 is not None:
            levelDensity = XYs1dModule.XYs1d(data=[[E0, 1.0/aveD], [domainMax, 1.0/aveD]],
                                           axes=XYs1dModule.XYs1d.defaultAxes(
                                               labelsUnits={
                                                    XYs1dModule.yAxisIndex: ('level_density', '1/eV'),
                                                    XYs1dModule.xAxisIndex: ('excitation_energy', 'eV')}))
        else:
            raise ValueError("Cannot set up levelDensity for GOE, need to specify domain and E0")

    # Generate the level energies
    # The level generator has a serious chance of making too many levels outside
    # of the energy range of interest so we filter them
    _energies = level_generator.getFakeLevelSequence(
        E0=E0,
        aveD=aveD,
        numLevels=numLevels,
        style=style,
        BrodyW=BrodyW,
        levelDensity=levelDensity)
    energies = numpy.array(
        [x for x in _energies if (domainMin is None or x >= domainMin) and (domainMax is None or x <= domainMax)])
    numLevels = len(energies)
    if verbose:
        print("Generated %d L=%s, J=%s resonances over the energy range %s to %s %s"
              % (numLevels, L, J, min(_energies), max(_energies), energyUnit))

    # Build the column headers
    columns = [tableModule.ColumnHeader(0, name='energy', unit=energyUnit),
               tableModule.ColumnHeader(1, name="L", unit=""),
               tableModule.ColumnHeader(2, name="J", unit="")]
    for iw, widthKey in enumerate(widthKeys):
        columns.append(tableModule.ColumnHeader(iw + 3, widthKey, unit=energyUnit))

    if DOTIMING:
        thisTime = datetime.datetime.now()
        print('\nenergies:', thisTime - lastTime, 's, numLevels=', numLevels)
        lastTime = thisTime

    # Sample the (scaled) widths and build the columns (vectorized with numpy trickery)
    # If the number of degrees of freedom is zero (e.g. for capture), then the
    # chi^2 distribution turns into a delta function.  That's really easy to sample from ;)
    widths = {"totalWidth": numpy.zeros_like(energies)}
    for widthKey in widthKeys:
        if widthKey == "totalWidth":
            continue
        else:
            widthValueCalculator = numpy.frompyfunc(aveWidthFuncs[widthKey].evaluate, 1, 1)
            if widthKey not in DOFs or DOFs[widthKey] == 0:
                widths[widthKey] = widthValueCalculator(energies)
            else:
                widths[widthKey] = (2.0 / DOFs[widthKey]) * \
                                   widthValueCalculator(energies) * \
                                   numpy.random.chisquare(DOFs[widthKey], size=numLevels) / 2.0
            widths["totalWidth"] = numpy.add(widths["totalWidth"], widths[widthKey])

    if DOTIMING:
        thisTime = datetime.datetime.now()
        print('widths:', thisTime - lastTime)
        lastTime = thisTime

    # Now build the table itself (gotta find a way to make this faster)
    resonances = tableModule.Table(columns=columns)
    for iE, E in enumerate(energies):
        row = [E, L, J]
        for widthKey in widthKeys:
            row.append(widths[widthKey][iE])
        if domainMin is not None and E < domainMin:
            continue
        if domainMax is not None and E > domainMax:
            continue
        resonances.addRow(row)

    if DOTIMING:
        thisTime = datetime.datetime.now()
        print('table:', thisTime - lastTime)
        lastTime = thisTime

    return resonances
