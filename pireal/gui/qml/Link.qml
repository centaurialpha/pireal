import QtQuick 2.9

Item {
    id: root

    property string title: ""
    property string link: ""

    implicitHeight: textLink.implicitHeight
    implicitWidth: textLink.implicitWidth

    SystemPalette { id: palette; colorGroup: SystemPalette.Active }

    Text {
        id: textLink
        text: title
        textFormat: Text.RichText
        color: palette.highlightedText
        font.pointSize: 12
    }

    MouseArea {
        id: ma
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: containsMouse ? Qt.PointingHandCursor : Qt.ArrowCursor
        onHoveredChanged: {
            textLink.font.underline = !textLink.font.underline
        }
        onClicked: Qt.openUrlExternally(link)
    }
}
