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
     id: container

     signal clicked
     property string text: "Button"

     smooth: true
     width: txtItem.width + 20; height: txtItem.height *2

     gradient: Gradient {
         GradientStop {
             position: 0
             color: "#fffbfb"
         }

         GradientStop {
             position: 1
             color: "#959595"
         }
     }


     MouseArea { id: mr; anchors.fill: parent; onClicked: container.clicked() }

     Text {
         id: txtItem; color: "#000000"; text: container.text; styleColor: "#cacaca"; anchors.centerIn: container;     }
 }
