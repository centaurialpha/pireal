import QtQuick 2.7

Rectangle {
    id: button

    signal clicked
    property alias texto: buttonText.text
    property int offset: 30

    border.color: "#ccc"

    width: buttonText.width + offset
    height: buttonText.height + offset

    Text {
        id: buttonText
        text: button.texto
        anchors.centerIn: parent
        color: "#5f6566"
    }

    MouseArea {
        anchors.fill: parent
        hoverEnabled: true

        onClicked: { button.clicked() }
        onEntered: { button.color = "#f5f5f5" }
        onExited: { button.color = "transparent" }
    }
}
