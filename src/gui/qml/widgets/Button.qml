import QtQuick 2.5

Rectangle {
    id: button

    signal clicked
    property alias texto: buttonText.text

    width: buttonText.width + 69
    height: buttonText.height + 10
//    radius: 3

    color: "#f1f1f1"
//    border.color: "#c4c7ca"

    scale: ma.pressed ? 0.95 : 1

    Text {
        id: buttonText
        text: button.texto
        font.pixelSize: 16
        anchors.centerIn: parent
        color: "#303336"
        renderType: Text.NativeRendering
    }

    MouseArea {
        id: ma

        anchors.fill: parent
        hoverEnabled: true

        onClicked: { button.clicked() }
    }
}
