/*
 Copyright (c) 2011 Nokia Corporation and/or its subsidiary(-ies).
 All rights reserved.
 This component and the accompanying materials are made available
 under the terms of the License "Eclipse Public License v1.0"
 which accompanies this distribution, and is available
 at the URL "http://www.eclipse.org/legal/epl-v10.html".

 Initial Contributors:
 Nokia Corporation - initial contribution.

 Contributors:

 Description:
*/


import Qt 4.7

Rectangle {
    width: 480
    color: "#6666DD"
    Column {
            TextEdit {
                id: title
                text: difftext
                wrapMode: TextEdit.WordWrap
                color: "white"
                font.bold: true
        }
     SButton {
         id: diffbutton
         text: "viewdiffs"
         onClicked: { controller.diff_viewer() }
     }
   }
}
