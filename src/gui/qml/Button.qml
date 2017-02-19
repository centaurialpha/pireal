import QtQuick 2.3

Rectangle {
    id: button

    color: "#7dbca9"
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
            button.color = "#5b8a7c"
        }

        onExited: {
            button.color = "#7dbca9"
        }

        onPressed: {
            button.color = "#5b8a7c"
        }

        onReleased: {
            button.color = "#7dbca9"
        }

        onClicked: {
            button.clicked()
        }

    }

}
