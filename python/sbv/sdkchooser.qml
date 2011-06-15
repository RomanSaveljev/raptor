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
    id: chooser
    width: 320
    color: "#666666"
    Component {
    id: sdkDelegate
        Rectangle {
            height: title.height
            width: parent.parent.width
            color: (model.dkchecked?"#808080":(((index %2) ==0?"#707070":"#606060")))
            Column {
            TextEdit {
                id: title
                text: model.sdk.path
                wrapMode: TextEdit.WordWrap
                color: "white"
                font.bold: true
             }
           }
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    sdk_controller.toggled(model.sdk)
                }
            }
        }
    }
  Row {
    ListView {
        id: sdkList
        height: chooser.height
        width: chooser.width-buttoncol.width
        model: pySDKListModel
        highlightFollowsCurrentItem: true

        delegate: sdkDelegate
    }


    Column {
        id: buttoncol
        SButton {
            id: diffbutton
            text: "diff"
            onClicked: { sdk_controller.diff() }
        }
        SButton {
            id: quitbutton
            text: "quit"
            onClicked:  sdk_controller.quit()
        }
    }
 }
}
