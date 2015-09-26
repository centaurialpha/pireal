import QtQuick 2.0

Rectangle {
    id: root

    color: "#F9F9F9";

    Image {
        id: logo

        anchors.centerIn: parent
        opacity: 0.2
        source: "../images/pireal_banner.png"

        SequentialAnimation on opacity {
            loops: Animation.Infinite
            PropertyAnimation { to: 0; duration: 2000 }
            PropertyAnimation { to: 0.2; duration: 2000 }

        }
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

