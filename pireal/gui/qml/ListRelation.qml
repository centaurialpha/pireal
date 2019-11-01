import QtQuick 2.7

Rectangle {
    id: root

    SystemPalette { id: darkPalette; colorGroup: SystemPalette.Active }

    color: darkPalette.base
    signal itemClicked(int index)

    function setTitle(title) {
        header.title = title;
    }

    // Component.onCompleted: relationModel.clear();

    Rectangle {
        id: header
        anchors.top: parent.top
        height: 30
        width: parent.width
        color: darkPalette.button
        property alias title: lblTitle.text
        Text {
            id: lblTitle
            text: ""
            font.bold: true
            font.pointSize: 12
            color: darkPalette.text
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
            }

            height: 70
            property bool current: ListView.isCurrentItem
            color: relationItem.current ? darkPalette.shadow : "transparent"

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
                    color: "#f1f1f1"
                }
                Text {
                    id: relationCard
                    color: "#a1a1a1"
                    text: qsTr("Cardinality: %1").arg(cardinality)
                }
                Text {
                    text: qsTr("Degree: %1").arg(degree)
                    color: "#a1a1a1"
                }
            }
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    relationView.currentIndex = index
                    root.itemClicked(index)
                }
            }
        }
    }
}
