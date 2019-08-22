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

"""
Fudge is a python package which allows one to view, plot and modify LLNL's evaluated nuclear data, and use LLNL's processing codes
that convert the evaluated data into processed data. Processed data is evaluatated nuclear transport data that has been converted into a format 
used by the deterministic (libndf.a) and and Monte Carlo (MCAPM) transport libraries. The deterministic library reads data
from the ndf files (ndf1, ndf2, etc.) and the Monte Carlo library reads data from the mcf files (mcf1.pdb, mcf2.pdb, etc.).

Getting at fudge's python scripts.
==================================
To use fudge, one must add the location of the fudge scripts to the environment variable PYTHONPATH. (PYTHONPATH is the environment variable
used by python when searching for imported python modules (files). On LLNL's computing system (LC) this would look something like,

export PYTHONPATH=$PYTHONPATH:/usr/apps/fudge/current/Src

for the bash shell.

Alternatively, one can add the following lines near the top of a python script (or type them at the prompt)

    >>> import sys
    >>> sys.path.append( "/usr/apps/fudge/current/Src" )

Other environment variables.
============================
Besides PYTHONPATH, there are four other environment variables used by fudge. They are::

    FUDGEPATH   Where fudges expects all platform dependent (e.g., binary) files to be.
    ENDLPATH    If defined, this is used to initialize fudgeDefaults.ENDL_DATABASE_DIR
    MCFPATH     If defined, this is used to initialize fudgeDefaults.MCF_DATABASE_DIR
    NDFPATH     If defined, this is used to initialize fudgeDefaults.NDF_DATABASE_DIR

If the environment variable FUDGEPATH is not set, fudge sets it to fudgeDefaults.DefaultFudgePath.
For more information on ENDL_DATABASE_DIR, MCF_DATABASE_DIR and NDF_DATABASE_DIR set the documentation
for the fudgeDefaults module.

Thus, there are three ways to set the variables fudge uses to search for files.

1) Do nothing and fudge will use the variables in the module fudgeDefaults.

2) Set the appropriate environment variable (i.e., FUDGEPATH, ENDLPATH, MCFPATH or NDFPATH).

3) Set variables in the fudgeDefaults module. For example,

>>> import fudgeDefaults
>>> fudgeDefaults.NDF_DATABASE_DIR = /my/personal/database/processed

Reading fudge's documentation.
==============================
In general, one should first instantiate an endlProject class object and work from it. For example the beginning of a fudge session may look like,

    >>> from fudge import *
    >>> project = endlProject( database = "endl99", workDir = "tmp" )

It is therefore important to read the documentation on the module endlProject; and in particular, the class endlProject.  
Also, see the module fudgeDefaults for default locations fudge searches to find evaluated and processed data files, 
and where it searches to find platform dependent files (e.g., executable files).
"""
