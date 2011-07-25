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
    color: "#6666DD"
    property string infotext: "blah"


    Component {
    id: buildDelegate

        Rectangle {
            height: title.height+4
            width: parent.parent.width
            color: (model.build.checked?"#8080DD":(((index %2) ==0?"#7070DD":"#6060DD")))
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
                    text: "Name: " + info + "; logpath: " + logpath
                    font.pointSize: 12
                    onTextChanged: controller.newlogpath(text)
                }
            }
        }
        Row {

            Column {

                ListView {
                    id: buildList
                    height: logchooser.height - logpath_area.height - infoarea.height
                    width: logchooser.width-buttoncol.width
                    model: pyBuildListModel
                    highlightFollowsCurrentItem: true

                    delegate: buildDelegate
                }
            }

            Column {
                id: buttoncol
                width: 100
                SButton {
                    id: nocleanbutton
                    width: parent.width
                    text: "noclean"
                    onClicked: { controller.filterclean() }
                }

                SButton {
                    id: nofailedbutton
                    width: parent.width
                    text: "nofailed"
                    onClicked: { controller.filternofailed();
                        console.log("Row number: ",row)
                    }
                }

                SButton {
                    id: unregister
                    text: "unregister this sdk"
                    onClicked: { controller.unregister();
                        window.close() }
                }
            }

        }

        Row {

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
}

