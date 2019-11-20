import QtQuick 2.7

Rectangle {
    id: root

    property bool closable: false

    SystemPalette { id: palette; colorGroup: SystemPalette.Active }

    color: palette.base

    signal itemClicked(int index)
    signal itemClosed (int index)

    function setTitle(title) {
        header.title = title;
    }

    function setClosable(value) {
        closable = value
    }

    Rectangle {
        id: header
        anchors.top: parent.top
        height: 30
        width: parent.width
        color: palette.button
        property alias title: lblTitle.text
        Text {
            id: lblTitle
            text: ""
            font.bold: true
            font.pointSize: 12
            color: palette.text
            anchors.centerIn: parent
        }
    }

    ListView {
        id: relationView
        anchors {
            top: header.bottom
            bottom: parent.bottom
            left: parent.left
            right: parent.right
            topMargin: 7
        }
        // TODO: hacer scrollbar sin Controls
        // ScrollBar.vertical: ScrollBar {}

        clip: true
        spacing: 3
        model: relationModel

        delegate: Rectangle {
            id: relationItem
            anchors {
                left: parent.left
                right: parent.right
                margins: 7
            }
            radius: 1
            height: 70
            property bool current: ListView.isCurrentItem
            color: relationItem.current ? palette.highlight : "transparent"

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    relationView.currentIndex = index
                    root.itemClicked(index)
                }
            }

            SequentialAnimation {
                id: closeAnimation
                PropertyAction { target: relationItem; property: "ListView.delayRemove"; value: true }
                NumberAnimation { target: relationItem; property: "scale"; to: 0; duration: 250; easing.type: Easing.InOutQuad }
                PropertyAction { target: relationItem; property: "ListView.delayRemove"; value: false }
            }

            Column {
                spacing: 5
                anchors.fill: parent
                anchors {
                    rightMargin: 10
                    leftMargin: 10
                    topMargin: 5
                    bottomMargin: 5
                }

                Text {
                    id: relationText
                    text: name
                    font.bold: true
                    font.pointSize: 12
                    color: palette.text
                }
                Text {
                    id: relationCard
                    color: palette.mid
                    text: qsTr("Cardinality: %1").arg(cardinality)
                }
                Text {
                    text: qsTr("Degree: %1").arg(degree)
                    color: palette.mid
                }
            }

            Image {
                source: "close.png"
                visible: closable && relationItem.current
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.margins: 8

                MouseArea {
                    id: ma
                    anchors.fill: parent
                    hoverEnabled: true
                    onClicked: {
                        itemClosed(index)
//                        closeAnimation.start()
                    }
                }
            }
        }
    }
}
