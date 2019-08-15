import QtQuick 2.7

Rectangle {
    id: root

    color: "#404244"

    ListView {
        id: relationView
        anchors.fill: parent
        clip: true
        spacing: 3
        model: relation_model
        delegate: Rectangle {
            id: relationItem
            anchors.left: parent.left
            anchors.right: parent.right
            height: 70
            property bool current: ListView.isCurrentItem
            color: relationItem.current ? "#262829" : "transparent"

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
                    backend.item_clicked(index)
                }
            }
        }
    }
}
