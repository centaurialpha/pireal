import QtQuick 2.9

Item {
    id: root

    property alias title: txtTitle.text
    property alias description: txtDescription.text

    implicitHeight: rec.implicitHeight
    implicitWidth: rec.implicitWidth

    width: rec.width
    height: rec.height

    SystemPalette { id: palette; colorGroup: SystemPalette.Active }

    Rectangle {
        id: rec
        color: palette.alternateBase
        height: 70
        width: root.width
        Column {
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.margins: 5
            anchors.verticalCenter: parent.verticalCenter
            spacing: 4
            Text {
                id: txtTitle
                color: palette.highlight
                font.pointSize: 10
            }

            Text {
                id: txtDescription
                color: palette.mid
                width: parent.width
                wrapMode: Text.Wrap
            }
        }
    }
}
