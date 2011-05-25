/*
* Copyright (c) 2011 Nokia Corporation and/or its subsidiary(-ies).
* All rights reserved.
* This component and the accompanying materials are made available
* under the terms of the License "Eclipse Public License v1.0"
* which accompanies this distribution, and is available
* at the URL "http://www.eclipse.org/legal/epl-v10.html".
*
* Initial Contributors:
* Nokia Corporation - initial contribution.
*
* Contributors:
*
* Description:
*
*/

#ifndef FILE_H_
#define FILE_H_

int is_file(char value[]);
char *get_cwd(void);
char *get_exe_location(void);
char *get_parent_dir(char dir[]);
char *path_join(char component1[], char component2[]);

#endif /* FILE_H_ */
