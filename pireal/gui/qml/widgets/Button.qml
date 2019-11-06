import QtQuick 2.7

Rectangle {
    id: button

    signal clicked
    property alias texto: buttonText.text
    property alias textColor: buttonText.color
    width: buttonText.width + 69
    height: buttonText.height + 10

    scale: ma.pressed ? 0.95 : 1

    Text {
        id: buttonText
        text: button.texto
        font.pixelSize: 16
        anchors.centerIn: parent
        renderType: Text.NativeRendering
    }

    MouseArea {
        id: ma

        anchors.fill: parent
        hoverEnabled: true

        onClicked: { button.clicked() }
    }
}
