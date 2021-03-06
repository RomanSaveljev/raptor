@rem
@rem Copyright (c) 2009 Nokia Corporation and/or its subsidiary(-ies).
@rem All rights reserved.
@rem This component and the accompanying materials are made available
@rem under the terms of the License "Eclipse Public License v1.0"
@rem which accompanies this distribution, and is available
@rem at the URL "http://www.eclipse.org/legal/epl-v10.html".
@rem
@rem Initial Contributors:
@rem Nokia Corporation - initial contribution.
@rem
@rem Contributors:
@rem
@rem Description: 
@rem

ECHO junk_file: this file is the dummy file to be used in the cp-testing. > junk_file
SET SBS_HOME=D:\yiluzhu\CBR\m04710\raptor
SET PATH=%SBS_HOME%\win32\mingw\bin;%SBS_HOME%\win32\msys\bin;%PATH%

@REM Generate the makefiles using case "all" ...
FOR %%c IN (all env echo cp sed) DO (
FOR %%i IN (100 200 500 750 1000 1250 1500 1750 2000 2250 2500) DO (
FOR %%d in (50 100) DO (
python makemakefile.py -t %%i -d %%d -m makefile_%%c_%%i_targets_%%d_divisions.mk)))

@REM Run mingw32-make with various values of j
FOR %%j in (10 25 50 75 100 250) DO (
FOR %%c IN (all env echo cp sed) DO (
FOR %%i IN (100 200 500 750 1000 1250 1500 1750 2000 2250 2500) DO (
FOR %%d in (50 100) DO (
make -j %%j -f makefile_%%c_%%i_targets_%%d_divisions.mk > makefile_%%c_%%i_targets_%%d_divisions_jobs_%%j.log 2>&1))))
