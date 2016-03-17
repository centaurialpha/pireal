import QtQuick 2.3

Rectangle {
    id: button

    color: "#f1f1f1"
    border.color: "lightgray"
    radius: 3
    property alias text: buttonText.text
    property alias pointSize: buttonText.font.pointSize
    property int textWidth: buttonText.width + 10
    signal clicked

    Text {
        id: buttonText
        anchors.centerIn: parent
        color: "#838b8c"
    }

    MouseArea {
        anchors.fill: parent
        hoverEnabled: true

        onEntered: {
            button.color = "#f7f7f7"
        }

        onExited: {
            button.color = "#f1f1f1"
        }

        onPressed: {
            button.color = "#e3e3e3"
        }

        onReleased: {
            button.color = "#f7f7f7"
        }

        onClicked: {
            button.clicked()
        }

    }

}
