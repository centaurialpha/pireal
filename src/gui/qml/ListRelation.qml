import QtQuick 2.6
import QtQuick.Controls 2.0


Rectangle {
    id: root

    signal itemClicked(int index)

    function addItem(item, cardinalidad, grado) {
        relationModel.append({"name": item, "cardinalidad": cardinalidad, "grado": grado});
    }

    function setTitle(title) {
        header.title = title;
    }

    function clear() {
        relationModel.clear();
    }

    function currentItem() {
        var index = relationView.currentIndex;
        var name = relationModel.get(index).name;
        return {"index": index, "name": name};
    }

    Component.onCompleted: clear();


    ListModel {
        id: relationModel
        ListElement {
            name: ""
            cardinalidad: 0
            grado: 0
        }
    }

    Rectangle {
        id: header
        anchors.top: parent.top
        height: 40
        width: parent.width
        color: "#aaa"
        property alias title: lblTitle.text
        Label {
            id: lblTitle
            text: "Relaciones"
            font.bold: true
            color: "white"
            anchors.centerIn: parent
            renderType: Label.NativeRendering
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
        ScrollBar.vertical: ScrollBar {}

        clip: true
        spacing: 3
        model: relationModel

        delegate: ItemDelegate {
            highlighted: ListView.isCurrentItem
            width: parent.width
            contentItem: Column {
                Label {
                    id: relationText
                    text: name
                    font.bold: true
                    font.pointSize: 12
                    renderType: Label.NativeRendering
                }
                Label {
                    id: relationCard
                    text: "Cardinalidad: " + cardinalidad
                    renderType: Label.NativeRendering
                }
                Label {
                    text: "Grado: " + grado
                    renderType: Label.NativeRendering
                }
            }
            onClicked: {
                relationView.currentIndex = index
                root.itemClicked(index)
            }
        }
    }
}
