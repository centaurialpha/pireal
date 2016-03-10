import QtQuick 2.3

Rectangle {
    id: root
    color: "#ededed"
    signal openDatabase(string path)
    signal newDatabase
    signal removeCurrent(string path)

    function loadItem(name, path) {
        listModel.append({"name": name, "path": path})
    }

    Component.onCompleted: {
        listModel.clear();
    }

    Rectangle {
        id: container
        anchors.centerIn: parent
        width: root.width / 2 ; height: root.height / 1.5
        color: "#f2f2f2"
        radius: 5
        border.color: "lightgray"

        Text {
            anchors.centerIn: parent
            font.pixelSize: 40
            font.bold: true
            color: "lightgray"
            text: qsTr("No recent databases")
            visible: listView.empty ? true : false;
        }

        ListModel {
            id: listModel

            ListElement {
                name: ""
                path: ""
            }
        }

        Component {
            id: delegate
            Item {
                id: listItem
                anchors {
                    left: parent.left
                    right: parent.right
                }
                property bool current: ListView.isCurrentItem


                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    onHoveredChanged:  {
                        listView.currentIndex = index;
                    }

                    onClicked: {
                        root.openDatabase(path)
                    }

                }

                Keys.onReturnPressed: {
                    root.openDatabase(path)
                }

                height: 75
                Column {
                    anchors {
                        fill: parent
                        leftMargin: 50
                    }

                    Text {
                        id: fileName
                        text: name
                        font.bold: true
                        font.pixelSize: 26
                        color: "#838b8c"

                    }

                    Text {
                        id: filePath
                        color: "#838b8c"
                        opacity: 0.5
                        text: path
                    }
                }

                Image {
                    id: imgDelete
                    source: "close.png"
                    anchors {
                        right: parent.right
                        verticalCenter: parent.verticalCenter
                        rightMargin: 15
                    }
                    visible: listItem.current ? true : false;
                    onVisibleChanged: NumberAnimation {
                        target: imgDelete; property: "scale"; from: 0; to: 1; duration: 200
                    }

                    MouseArea {
                        anchors.fill: parent

                        onClicked: {
                            root.removeCurrent(path);
                            listView.model.remove(index);
                        }
                    }
                }
            }
        }

        Component {
            id: high
            Rectangle {

                color: "#e3e3e3"
                anchors {
                    left: high.left
                    right: high.right
                }

            }
        }

        ListView {
            id: listView

            anchors.fill: parent
            width: parent.width / 2.5; height: parent.height / 1.5
            model: listModel
            delegate: delegate
            highlight: high
            focus: true
            property bool empty: listView.count == 0
        }
    }

    Row {
        anchors {
            horizontalCenter: container.horizontalCenter
            bottom: container.top
            bottomMargin: 10
        }

        Text {
            id: title

            text: qsTr("Opens a recent database or ")
            color: "#838b8c"
            font.pixelSize: 16
        }

        Button {
            text: qsTr("Create a new database")
            anchors.verticalCenter: title.verticalCenter
            width: 150; height: 40
            pointSize: 10

            onClicked: {
                root.newDatabase();
            }
        }
    }

    Row {
        anchors {
            bottom: parent.bottom
            right: parent.right
            bottomMargin: 5
            rightMargin: 10
        }

        Text {
         text: "Powered by: "
         height: logoPython.height
         verticalAlignment: Text.AlignVCenter
        }

        Image { id: logoPython; source: "python-logo.png"; opacity: 0.7 }
        Image { source: "qt-logo.png"; opacity: 0.7 }
    }


}
