import QtQuick 2.0

Rectangle {
    id: root

    color: "#F9F9F9";

    Image {
        id: icon

        anchors.left: parent.left
        anchors.leftMargin: parent.width / 4
        anchors.verticalCenter: parent.verticalCenter
        opacity: 0.2
        source: "../images/icon.png"
        width: 128; height: 128

        transform: Rotation {
            id: rotation
            origin.x: icon.width / 2
            origin.y: icon.height / 2
            axis.x: 0; axis.y: 1; axis.z: 0
            angle: 0
        }

        NumberAnimation {
            target: rotation
            property: "angle"
            from: 0; to: 360; duration: 1050
            running: true
            loops: Animation.Infinite
        }

    }

    Image {
        id: logo

        opacity: 0.2
        source: "../images/pi.png"
        anchors.left: icon.right
        anchors.top: icon.top
        anchors.topMargin: -10
        anchors.leftMargin: 50
    }

    Text {
        text: "Copyright © 2015 - Pireal under GPLv3+ License"
        font.pointSize: 10
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.bottomMargin: 10
        anchors.leftMargin: 10
    }

    Row {
        anchors.bottomMargin: 5
        anchors.rightMargin: 10
        anchors.bottom: parent.bottom
        anchors.right: parent.right

        Text {
            text: "Powered by: ";
            height: logoPython.height;
            verticalAlignment: Text.AlignVCenter;
        }

        Image { id: logoPython; source: "../images/python-logo.png"; }
        Image { source: "../images/qt-logo.png"; }
    }
}

