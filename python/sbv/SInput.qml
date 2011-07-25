import QtQuick 1.0

Rectangle {
    id: s_input
    color: "#ffffe4"
    width: parent.width/2
    height: parent.height

    TextInput {
        id: input_field;
        text: "";
        width: parent.width;
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
        selectByMouse: true;
        readOnly: false
    }

    property alias text: input_field.text

    MouseArea {
        anchors.fill: parent

        onClicked: {
            if (!input_field.activeFocus) {
                input_field.forceActiveFocus();
                input_field.openSoftwareInputPanel();
            } else {
                input_field.focus = false;
            }
        }
        onPressAndHold: input_field.closeSoftwareInputPanel();
    }
}
