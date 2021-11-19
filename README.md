# FUDGE (For Updating Data and Generating Evaluations)

**FUDGE** is a nuclear data package built around Python that supports reading, viewing, modifying,
writing and processing of nuclear data in the **GNDS** format.

The current release of **FUDGE** focuses on supporting version 2.0 of the Generalized Nuclear Database Structure (**GNDS**).
The **FUDGE** package includes tools to translate other nuclear data formats to and from **GNDS**,
plus tools for testing, visualizing, and processing **GNDS** data.

# Contents of this README:

    - Getting Started
    - Basic Use (translating ENDF files)
    - Getting Help

## Getting Started:

Installing **FUDGE** only requires Python (version 3.6 or higher) and NumPy (version 1.15 or higher).
The following installation options are currently supported:

    - Installation via `pip install`: This is ideal for use in virtual environments. The 
      following steps are recommended to `pip install` FUDGE:

        (i)  Ensure that NumPy (version 1.15 or higher) and wheels are installed in your 
             Python environment

        (ii) Run the following `pip install` command:
                 pip install git+https://github.com/LLNL/fudge.git@5.0.0

    - Installation via cloning the git repository and building with the unix `make` command: 
      This is the typical development mode for active FUDGE maintenance and improvements.
      The following steps are recommended:

        (i)   Ensure that NumPy (version 1.15 or higher) is installed

        (ii)  Run the following `git clone` command to clone FUDGE to the current directory: 
                  git clone git@github.com:LLNL/fudge.git

        (iii) Build FUDGE with the following `make` command:
                  cd fudge; make -s

        (iv)  [Optional] Setting environment variables: for general use of the FUDGE package, 
              some changes should be made to your computer's environment. The following lines 
              make the required change. Note that <path_to_FUDGE> indicates the path to the 
              directory containing this README.md file:

              on unix with the bash, ksh, or similar shell, put the following line in the 
              .bashrc or equivalent file:
                  export PYTHONPATH=$PYTHONPATH:<path_to_FUDGE>

              on csh, tcsh or similar shell into the appropriate shell file:
                  setenv PYTHONPATH $PYTHONPATH:<path_to_FUDGE>

              on Windows, the environment variable should be added to the registry (see for 
              example <http://www.support.tabs3.com/main/R10463.htm>)

## Requirements for interactive plotting

When **FUDGE** was updated to Python3 its interactive plotting was updated to use
**matplotlib** and **PyQt5** (the Python2 version used **Gnuplot** and **Tkinter** for interactive plotting).
While **PyQt5** is not a requirement for installing **FUDGE**, it is needed to use the new interactive 
plotting module.

## Basic Use:

After installing **FUDGE**, a user may be interested in translates a **ENDF-6** file into a **GNDS** file and vice versa.
Two tools for translating **GNDS** files to and from **ENDF-6** files are included in the *brownies/bin* directory.

The Python script **brownies/bin/endf2gnds.py** translations an **ENDF-6** file to a **GNDS** file. 
This script writes a **GNDS** file containing the **reactionSuite** node and, if covariance data are 
present in the ENDF-6 file, its also writes a **GNDS** file containing the **covarianceSuite** node. For example,
the following command translating the **ENDF/B-VIII.0** file 
*n-001_H_001.endf* and outputs the files n-001_H_001.xml and n-001_H_001-covar.xml:
```
<path_to_FUDGE>/brownies/bin/endf2gnds.py n-001_H_001.endf n-001_H_001.xml
```
The above command can be used when **FUDGE** is installed using the `git clone` as described above. For the `pip install`
installation the command is
```
brownies/bin/endf2gnds.py n-001_H_001.endf n-001_H_001.xml
```
Ergo, the path *<path_to_FUDGE>/* is not used. This goes for the other examples below.

The Python script **brownies/bin/gnds2endf.py** translations a **GNDS** file to an **ENDF-6** file. This
script will look for a corresponding covariance file and, if present, add its data to the outputted **ENDF-6** 
file. For example, the following translates the *n-001_H_001.xml* file generated in the **endf2gnds.py** comannd above 
back into an **ENDF-6** file:
```
<path_to_FUDGE>/brownies/bin/gnds2endf.py n-001_H_001.xml
```

**FUDGE** scripts use the **argparse.py** module to parse input arguments. To get *help* on a script, run the script
with the *-h* option. For example, to get help on the usage of the *bin/processProtare.py* script execute:
```
<path_to_FUDGE>/bin/processProtare.py -h
```

There are more scripts in the *bin* directory that a user may find useful. One can also run **FUDGE** interactively.
The following Python commands show how to read in the *n-001_H_001.xml* generated by the example above, print a list
of its reactions and plot each reaction's cross section on a single plot:
```
from fudge import reactionSuite     # FUDGE must be in the PYTHONPATH.
n_H1 = reactionSuite.readXML( 'n-001_H_001.xml' )
for reaction in n_H1.reactions: print( reaction )

crossSections = []
for reaction in n_H1.reactions:
    crossSection = reaction.crossSection.toPointwise_withLinearXYs( lowerEps = 1e-7 )
    crossSection.plotLegendKey = str( reaction )
    crossSections.append( crossSection )

crossSection.multiPlot( crossSections, rangeMin = 1e-5, xylog = 3,
        title = 'n + U230', xLabel = 'Neutron energy [eV]', yLabel = 'Cross section [b]' )
```

## Getting Help:

**FUDGE** documentation is currently undergoing an update but some documentation can be found by executing the following
**make** command in the **FUDGE** directory:
```
make -s docs
```
To view the documentation, open the file *doc/sphinx/_build/html/index.html* inside the **FUDGE** directory.

For other questions about the **FUDGE**, please feel free to contact the maintainers at <mattoon1@llnl.gov>, *beck6@llnl.gov*
or *gert1@llnl.gov*.

# License

**FUDGE** is distributed under the terms of the 3-clause BSD license.

All new contributions must be made under the 3-clause BSD license.

See LICENSE, COPYRIGHT and NOTICE for details.

SPDX-Licence-Identifier: BSD-3-Clause

This package includes several components:  
LLNL-CODE-683960	(FUDGE)

LLNL-CODE-770134	(numericalFunctions  
LLNL-CODE-771182	(statusMessageReporting)  
LLNL-CODE-725546	(Merced)

**FUDGE** is a product of the Nuclear Data and Theory Group at Lawrence Livermore National Laboratory (LLNL).

This work was performed under the auspices of the U.S. Department of Energy by Lawrence Livermore National Laboratory
under Contract DE-AC52-07NA27344.
