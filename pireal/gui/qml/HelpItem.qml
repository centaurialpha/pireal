import QtQuick 2.9

Item {
    id: root

    property alias title: txtTitle.title
    property alias description: txtDescription.text
    property alias link: txtTitle.link

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

            Link { id: txtTitle  }

            Text {
                id: txtDescription
                color: palette.mid
                width: parent.width
                wrapMode: Text.Wrap
            }
        }
    }
}
