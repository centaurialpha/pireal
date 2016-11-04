import QtQuick 2.3

Rectangle {
    id: button

    color: "#8fb7e7"
    scale: mouseArea.pressed ? 0.9 : 1
    radius: 3
    property alias text: buttonText.text
    property alias pointSize: buttonText.font.pointSize
    property int textWidth: buttonText.width + 10
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
            button.color = "#a1c1e7"
        }

        onExited: {
            button.color = "#8fb7e7"
        }

        onPressed: {
            button.color = "#708fb5"
        }

        onReleased: {
            button.color = "#8fb7e7"
        }

        onClicked: {
            button.clicked()
        }

    }

}
