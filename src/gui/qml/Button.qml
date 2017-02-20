import QtQuick 2.3

Rectangle {
    id: button

    color: "#91a7ff"
    scale: mouseArea.pressed ? 0.9 : 1
    radius: 3
    property alias text: buttonText.text
    property alias pointSize: buttonText.font.pointSize
    property int textWidth: buttonText.width + 10
    property color darkColor: Qt.lighter("#91a7ff", 0.9)
    signal clicked

    Text {
        id: buttonText
        anchors.centerIn: parent
        color: "white"
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: true

        onEntered: {
            button.color = darkColor
        }

        onExited: {
            button.color = "#91a7ff"
        }

        onPressed: {
            button.color = darkColor
        }

        onReleased: {
            button.color = "#91a7ff"
        }

        onClicked: {
            button.clicked()
        }

    }

}
