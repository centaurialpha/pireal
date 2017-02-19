/*
 * Copyright 2015-2016 - Gabriel Acosta <acostadariogabriel@gmail.com>
 *
 * This file is part of Pireal.
 *
 * Pireal is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * any later version.
 *
 * Pireal is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Pireal; If not, see <http://www.gnu.org/licenses/>.
 */

import QtQuick 2.3


Rectangle {
    id: root
    color: "#ffffff"
    property bool compressed: false
    signal openDatabase(string path)
    signal newDatabase
    signal removeCurrent(string path)

    function loadItem(name, path) {
        listModel.append({"name": name, "path": path})
    }

    function clear() {
        listModel.clear();
    }

    ListModel {
        id: listModel

        ListElement {
            name: ""
            path: ""
        }
    }

    Component.onCompleted: {
        listModel.clear();
    }

    onWidthChanged: {
        if(root.width < 900) {
            root.compressed = true;
        } else {
            root.compressed = false;
        }
    }

    Rectangle {
        anchors {
            right: parent.right
            top: parent.top
            margins: 10
        }
        color: "#7dbca9"
        width: 30
        height: 30
        radius: width / 2
        scale: maarea.pressed ? 0.8 : 1

        Text {
            text: "?"
            color: "white"
            anchors.centerIn: parent
        }

        MouseArea {
            id: maarea
            anchors.fill: parent
            onClicked: {
                flipArea.flipped = !flipArea.flipped;
            }

        }
    }


    Flipable {
        id: flipArea
        width: root.width / 2; height: root.height / 1.5
        anchors.centerIn: parent
        property bool flipped: false

        transform: Rotation {
            id: rotation
            origin.x: flipArea.width / 2
            origin.y: flipArea.height / 2
            axis.x: 0; axis.y: 1; axis.z: 0
            angle: 0
        }

        states: State {
            name: "back"
            PropertyChanges { target: rotation; angle: 180 }
            when: flipArea.flipped
        }

        transitions: Transition {
            NumberAnimation { target: rotation; property: "angle"; duration: 500 }
        }

        front: Rectangle {
            id: container
            anchors.fill: parent
            color: "#f5f5f5"
            border.color: "#dddddd"
            border.width: 1
            enabled: !parent.flipped
            radius: 3

            ListView {
                id: listView

                anchors {
                    topMargin: 5
                    fill: parent
                }
                width: parent.width / 2.5; height: parent.height / 1.5
                model: listModel
                spacing: 3
                focus: true
                clip: true
                currentIndex: -1
                property bool empty: listView.count == 0
                delegate: Rectangle {
                    id: listItem
                    anchors {
                        left: parent.left
                        right: parent.right
                        leftMargin: 5
                        rightMargin: 5
                    }
                    height: 75
                    property bool current: ListView.isCurrentItem
                    color: listItem.current ? "#7dbca9" : "#ebebeb"
                    MouseArea {
                        anchors.fill: parent
                        hoverEnabled: true

                        onHoveredChanged: {
                            listView.currentIndex = index;
                        }

                        onExited: {
                            listView.currentIndex = -1;
                        }

                        onClicked: {
                            root.openDatabase(path);
                        }
                    }

                    Behavior on color {
                        NumberAnimation {
                            target: listItem
                            property: "opacity"
                            from: 0.7
                            to: 1
                            duration: 300
                        }
                    }

                    Column {
                        anchors {
                            verticalCenter: parent.verticalCenter
                            left: parent.left
                            right: parent.right
                            leftMargin: 20
                            rightMargin: 20
                        }

                        Text {
                            text: name
                            font.bold: true
                            font.pixelSize: 30
                            color: listItem.current ? "#fafbfb" : "#979dac"
                        }

                        Text {
                            text: path
                            color:listItem.current ? "#fafbfb" : "#979dac"
                            width: parent.width
                            elide: Text.ElideLeft
                        }
                    }

                    Image {
                        id: imgDelete
                        source: "close.png"
                        anchors {
                            right: parent.right
                            top: parent.top
                            topMargin: 15
                            rightMargin: 15
                        }
                        scale: ma.pressed ? 0.7 : 1
                        visible: listItem.current ? true: false
                        onVisibleChanged: NumberAnimation {
                            target: imgDelete; property: "scale"; from: 0; to: 1; duration: 200
                        }

                        MouseArea {
                            id: ma
                            anchors.fill: parent
                            onClicked: {
                                root.removeCurrent(path);
                                listView.model.remove(index);
                            }
                        }
                    }
                }
            }
        }

        back: Rectangle {
            id: backContainer
            enabled: parent.flipped
            color: "#f5f5f5"
            border.color: "#dddddd"
            anchors.fill: parent
            radius: 3

            Flickable {
                interactive: true
                clip: true
                anchors.fill: backContainer
                contentHeight: col.height
                boundsBehavior: Flickable.StopAtBounds
                Column {
                    id: col
                    spacing: 15
                    anchors {
                        left: parent.left
                        right: parent.right
                        margins: 10
                    }
                }
            }
        }
    }

    Row {
        anchors {
            horizontalCenter: flipArea.horizontalCenter
            bottom: flipArea.top
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
            width: textWidth; height: 40
            pointSize: 10

            onClicked: {
                root.newDatabase();
            }
        }
    }

    Row {
        spacing: 10
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
         font.pixelSize: 12
        }

        Image { id: logoPython; source: "python-logo.png"; opacity: 0.7 }
        Image { source: "bwqt.png"; opacity: 0.7 }
    }

    Text {
        text: "Copyright © 2015-" + new Date().getFullYear() + " Gabriel Acosta. Pireal is distributed under the terms of the GNU GPLv3+ copyleft license"
        anchors {
            bottom: parent.bottom
            left: parent.left
            bottomMargin: 5
            leftMargin: 10
        }
        font.pixelSize: 12
        visible: root.compressed ? false : true
    }


}
