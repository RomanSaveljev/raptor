@rem
@rem Copyright (c) 2005-2011 Nokia Corporation and/or its subsidiary(-ies).
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
@SET SBS=%~dp0sbs.bat
@CALL "%~dp0sbs_env.bat"

@REM Run Raptor with all the arguments.
@%__PYTHON__% %SBS_HOME%\bin\sbs.py %*

@ENDLOCAL
@cmd /c exit /b %ERRORLEVEL%
