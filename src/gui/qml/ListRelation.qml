import QtQuick 2.6
import QtQuick.Controls 2.0


Rectangle {
    id: root

    color: "#423d4c"
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

    function hasItem() {
        return relationModel.count > 0;
    }

    function currentItemText() {
        var index = relationView.currentIndex;
        var item = relationModel.get(index);
        var text = "";
        if ( item !== undefined)
            text = item.name;
        return text;
    }

    function setCardinality(value) {
        var item = relationModel.get(relationView.currentIndex);
        item.cardinalidad = value;
    }

    function currentIndex() {
        return relationView.currentIndex;
    }

    function currentItem() {
        var index = relationView.currentIndex;
        var item = relationModel.get(index);
        var name = "";
        if (item !== undefined) {
            name = relationModel.get(index).name;
        }
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
        height: 30
        width: parent.width
        color: "#423d4c"
        property alias title: lblTitle.text
        Label {
            id: lblTitle
            text: "Relaciones"
            font.bold: true
            font.pointSize: 12
            color: "#f9f9f9"
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
            Binding {
                target: background
                property: "color"
                value: "#54505c"
            }

            contentItem: Column {
                spacing: 5
                Label {
                    id: relationText
                    text: name
                    font.bold: true
                    font.pointSize: 12
                    color: "#f9f9f9"
                    renderType: Label.NativeRendering
                }
                Label {
                    id: relationCard
                    text: "Cardinalidad: " + cardinalidad
                    color: "#a1a1a1"
                    renderType: Label.NativeRendering
                }
                Label {
                    text: "Grado: " + grado
                    color: "#a1a1a1"
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
