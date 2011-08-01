import QtQuick 1.0

Rectangle {
    id: small_label
    width: parent.width
    height: parent.height
    color: "#ffffe4"

    property double scaling_factor: 0.8

    Text {
        id: text_string
        text: "Small label default text"
        wrapMode: Text.WrapAtWordBoundaryOrAnywhere
        horizontalAlignment: Text.AlignLeft
        width: parent.width

        anchors.centerIn: parent; anchors.verticalCenterOffset: -1
        font.pixelSize: scaling_factor*(parent.width > parent.height ? Math.min(parent.width, parent.height)*0.3 :
              ( parent.width == parent.height ? Math.min(parent.width, parent.height)*0.12 : Math.min(parent.width, parent.height)*0.167 ))
        style: Text.Sunken
        color: "black"
        styleColor: "black"
        smooth: true
    }

    property alias text: text_string.text

    MouseArea {
        anchors.fill: parent
    }
}
