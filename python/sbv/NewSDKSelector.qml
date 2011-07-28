import QtQuick 1.0

Rectangle {
    id: new_sdk_selector
    width: 400
    height: 120
    x: 0
    y: 0
    z: -1
    state: "on"

    Column {
        id: column1
        anchors.fill: parent

        Row {
            id: row1
            y: 0
            height: new_sdk_selector.height/6
            anchors.right: parent.right
            anchors.rightMargin: 0
            anchors.left: parent.left
            anchors.leftMargin: 0

            SmallLabel {
                id: info_label
                width: row1.width/2
                height: parent.height
                color: "#ffffe4"
                text: "Enter a tag for the SDK (optional):"
            }

            SInput {
                id: info_input
                color: "#fafadf"
                width: row1.width/2
                height: parent.height
            }
        }

        Row {
            id: row2
            y: new_sdk_selector.height/6
            height: new_sdk_selector.height/6
            anchors.right: parent.right
            anchors.rightMargin: 0
            anchors.left: parent.left
            anchors.leftMargin: 0

            SmallLabel {
                id: epocroot_label
                width: row2.width/2
                height: parent.height
                color: "#ffff85"
                text: "Enter EPOCROOT for this SDK:"
            }

            SInput {
                id: epocroot_input
                color: "#fafa80"
                width: row2.width/2
                height: parent.height
            }
        }

        Row {
            id: row3
            y: 2*new_sdk_selector.height/6
            height: new_sdk_selector.height/3
            anchors.right: parent.right
            anchors.rightMargin: 0
            anchors.left: parent.left
            anchors.leftMargin: 0

            SmallLabel {
                id: logpath_label
                width: row3.width/2
                height: parent.height
                color: "#ffffe4"
                text: "Enter the log directory for this SDK (defaults to $EPOCROOT/epoc32/build):"
                scaling_factor: 0.4
            }

            SInput {
                id: logpath_input
                color: "#fafadf"
                width: row3.width/2
                height: parent.height
                scaling_factor: 0.4
            }
        }

        Row {
            id: row4
            y: 4*new_sdk_selector.height/6
            height: new_sdk_selector.height/3
            anchors.right: parent.right
            anchors.rightMargin: 0
            anchors.left: parent.left
            anchors.leftMargin: 0

            Rectangle {
                id: rectangle4_1
                color: "#b9f3bb"
                width: row4.width/2
                height: parent.height

                Text {
                    id: okay
                    text: "Okay"

                    anchors.centerIn: parent; anchors.verticalCenterOffset: -1
                    font.pixelSize: parent.width > parent.height ? Math.min(parent.width, parent.height)*0.3 :
                                                                                                             ( parent.width == parent.height ? Math.min(parent.width, parent.height)*0.12 : Math.min(parent.width, parent.height)*0.167 )
                    style: Text.Sunken; color: "black"; styleColor: "black"; smooth: true
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        console.log("Okayed new SDK :-).");
                        console.log(info_input.text);
                        console.log(epocroot_input.text);
                        console.log(logpath_input.text);
                        console.log(sdk_controller);
                        sdk_controller.add_sdk(info_input.text, epocroot_input.text, logpath_input.text);
                        new_sdk_selector.state = "off";

                        // Clear the input fields for next time
                        info_input.text = ""
                        epocroot_input.text = ""
                        logpath_input.text = ""

                    }
                }
            }

            Rectangle {
                id: rectangle4_2
                color: "#f9a9a9"
                width: row4.width/2
                height: parent.height

                Text {
                    id: cancel
                    text: "Cancel"

                    anchors.centerIn: parent; anchors.verticalCenterOffset: -1
                    font.pixelSize: parent.width > parent.height ? Math.min(parent.width, parent.height)*0.3 :
                                                                                                             ( parent.width == parent.height ? Math.min(parent.width, parent.height)*0.12 : Math.min(parent.width, parent.height)*0.167 )
                    style: Text.Sunken; color: "black"; styleColor: "black"; smooth: true
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        console.log("Cancelled addition of new SDK :-).");
                        new_sdk_selector.state = "off";
                    }
                }
            }
        }
    }
    states: [
        State {
            name: "off"
            PropertyChanges {
                target: new_sdk_selector;
                z:-1
            }
        },
            State {
                name: "on"
                PropertyChanges {
                    target: new_sdk_selector;
                    z:1
                }
        }

    ]
}
