import QtQuick 1.0

Rectangle {
    id: s_input
    color: "#ffffe4"
    width: parent.width/2
    height: parent.height
    property double scaling_factor: 0.8

    TextInput {
        id: input_field;
        anchors.fill: parent;
        text: "";
        width: parent.width;
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
        selectByMouse: true;
        readOnly: false
        font.pixelSize: scaling_factor*(parent.width > parent.height ? Math.min(parent.width, parent.height)*0.3 :
              ( parent.width == parent.height ? Math.min(parent.width, parent.height)*0.12 : Math.min(parent.width, parent.height)*0.167 ))
    }

    property alias text: input_field.text
    property alias pixelSize: input_field.font.pixelSize

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
