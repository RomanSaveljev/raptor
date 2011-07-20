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
    height: 122
    color: "white"
    Component {
        id: sdkDelegate
        Rectangle {
            height: title.height
            width: parent.parent.width
            color: (model.dkchecked?"#CAEDFF":(((index %2) ==0?"#F5FFBF":"#BFF5FF")))
            Column {
                TextEdit {
                    id: title
                    text: model.sdk.path
                    wrapMode: TextEdit.WordWrap
                    color: "black"
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

    Column
    {
        height: 122
        Row {
            height: 0
            Rectangle {
                id: titleRect
                color: "white"
                Text {
                    id: text1
                    width: chooser.width - buttoncol.width
                    text: "Available SDKs"
                    font.pixelSize: 18
                    color: "#4B2DC2"
                }

            }
        }

        Row {
            x: 0
            y: 22
            height: 122
            ListView {
                id: sdkList
                y: 22
                width: chooser.width - buttoncol.width
                height: 100
                model: pySDKListModel
                highlightFollowsCurrentItem: true

                delegate: sdkDelegate
            }
        }
    }
    Column {
        id: buttoncol
        x: 240
        y: 0
        width: 90
        anchors.right: parent.right
        anchors.rightMargin: 0
        SButton {
            id: sdkregister
            width: parent.width
            text: "Add SDK..."
            onClicked: { sdk_controller.add_sdk() }
        }
        SButton {
            id: diffbutton
            width: parent.width
            text: "diff"
            onClicked: { sdk_controller.diff() }
        }
        SButton {
            id: quitbutton
            width: parent.width
            text: "quit"
            onClicked:  sdk_controller.quit()
        }
    }
}
