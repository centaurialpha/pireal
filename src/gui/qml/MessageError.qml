import QtQuick 2.6
import "widgets"

Rectangle {
    id: root

    color: "#e3757e"
    width: 350; height: 150;
    radius: 1
    border.color: "#a0a0a0"

    property bool syntaxError: true
    signal close;

    function setMessageType(isSyntaxEror) {
        syntaxError = isSyntaxEror;
    }

    function setMessage(text) {
        msg.text = text;
    }

    Text {
        id: title
        text: root.syntaxError ? qsTr("Syntax Error") : qsTr("Query Error")
        color: "white"
        font.bold: true
        font.pixelSize: 20
        anchors {
            bottom: body.top
            left: parent.left
            leftMargin: 5
            bottomMargin: 5

        }
    }

    Rectangle {
        id: body
        anchors {
            bottom: root.bottom
            left: root.left
            right: root.right
            leftMargin: 1
            rightMargin: 1
            bottomMargin: 1
        }
        color: "white"
        height: root.height / 2 + 40

        Rectangle {
            color: "white"
            anchors {
                left: parent.left
                right: parent.right
                leftMargin: 30
                rightMargin: 30
            }
            height: parent.height - btn.height

            Text {
                id: msg
                text: ""
                anchors.centerIn: parent
                font.pixelSize: 16
                width: parent.width
                wrapMode: Text.WrapAnywhere
                color: "gray"
            }
        }
    }

    Button {
        id: btn

        text: qsTr("Done")
        anchors {
            left: parent.left
            right: parent.right
            bottom: parent.bottom
            margins: 1
        }

        onClicked: {
            close();
        }
    }
}
