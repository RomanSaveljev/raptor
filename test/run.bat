@rem
@rem Copyright (c) 2005-2010 Nokia Corporation and/or its subsidiary(-ies).
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

@SETLOCAL
@CALL %SBS_HOME%\bin\sbs_env.bat

@SET __TEST_SUITE__=%SBS_HOME%\test\common\run_tests.py

@REM Then run the test suite with all the arguments
@%__PYTHON__% -tt %__TEST_SUITE__% %*

@ENDLOCAL

@CMD /C EXIT /B %ERRORLEVEL%
