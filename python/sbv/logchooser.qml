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
    id: logchooser
    width: 480
    color: "#666666"
    property string infotext: "blah"


    Component {
    id: buildDelegate

        Rectangle {
            height: title.height+4
            width: parent.parent.width
            color: (model.build.checked?"#808080":(((index %2) ==0?"#707070":"#606060")))
            Column {
            Text {
                id: title
                elide: Text.ElideRight
                text: model.build.name
                color: "white"
                font.bold: true
             }
            Text {
                id: info
                elide: Text.ElideRight
                text: model.build.info
                color: "white"
                font.bold: true
                visible: false
             }
           }
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    controller.toggled(model.build)
                    if (info.visible) {
                        info.visible = false
                        parent.height = title.height + 4
                    } else {
                        info.visible = true
                        parent.height = title.height + info.height + 4
                    }
                }
            }
        }
    }

    Column {
        Row {
            Rectangle {
                id: logpath_area
                width: logchooser.width
                height: 20
                color: "white"
                TextEdit {
                    id: logpath_edit
                    width: logchooser.width
                    text: logpath
                    font.pointSize: 12
                    onTextChanged: controller.newlogpath(text)
                }
            }
        }
        Row {

            ListView {
                id: buildList
                height: logchooser.height - logpath_area.height - infoarea.height
                width: logchooser.width-buttoncol.width
                model: pyBuildListModel
                highlightFollowsCurrentItem: true

                delegate: buildDelegate
            }

            Column {
                id: buttoncol
                SButton {
                    id: diffbutton
                    text: "noclean"
                    onClicked: { controller.filterclean() }
                }
                SButton {
                    id: quitbutton
                    text: "nofailed"
                    onClicked:  controller.filternofailed()
                }
            }
        }

        Rectangle {
            id: infoarea
            height: 100
            width: logchooser.width
            color: "white"
            TextEdit {
                text: controller.info
                wrapMode: TextEdit.WordWrap
                anchors.fill: parent
                font.pointSize: 12
            }

        }
    }
}

