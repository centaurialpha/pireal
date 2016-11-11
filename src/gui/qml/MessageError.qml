import QtQuick 2.3

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

    Rectangle {
        id: btn
        anchors {
            bottom: root.bottom
            left: root.left
            right: root.right
            leftMargin: 1
            rightMargin: 1
            bottomMargin: 1
        }
        color: "#f5f5f5"
        height: root.height / 5
        scale: ma.pressed ? 0.9 : 1

        Text {
            text: qsTr("Done");
            font.pixelSize: 24
            font.bold: true
            color: "gray"
            anchors.centerIn: parent
        }

        MouseArea {
            id: ma
            anchors.fill: parent
            onClicked: {
                root.close();
            }
        }
    }
}
