import QtQuick 2.9

Item {
    id: root

    implicitWidth: background.implicitWidth
    implicitHeight: background.implicitHeight
    height: buttonText.height + 20
    width: 110

    property alias color: background.color;
    property alias text: buttonText.text
    property alias textColor: buttonText.color
    property alias radius: background.radius

    scale: ma.pressed ? 0.90 : 1
    signal clicked

    SystemPalette { id: palette; colorGroup: SystemPalette.Active }

    Rectangle {
        id: background
        anchors.fill: parent
        radius: 2
    }

    Text {
        id: buttonText
        anchors.centerIn: parent
    }

    MouseArea {
        id: ma

        anchors.fill: parent
        onClicked: root.clicked()

        onPressed: {
            background.color = Qt.lighter(palette.button)
        }

        onReleased: {
            background.color = palette.button
        }
    }

}
