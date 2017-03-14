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

import QtQuick 2.6
import QtQuick.Layouts 1.1
import "widgets"

Item {
    id: root

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
        if(root.width < 1022) {
            root.compressed = true;
        } else {
            root.compressed = false;
        }
    }

    RowLayout {
        anchors.fill: parent

        Rectangle {
            id: leftArea



            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.maximumWidth: 400
            visible: root.compressed ? false : true

            Image {
                id: logo
                source: "pireal_logo-black.png"
                anchors.horizontalCenter: parent.horizontalCenter
            }

            Text {
                id: whatIsPireal
                text: qsTr("<b>π</b>real is a teaching tool for use in learning introduction to database. It allows the user to interactively experiment with Relational Algebra.")
                anchors.top: logo.bottom
                anchors.left: parent.left
                anchors.right: separator.left
                anchors.margins: 20
                wrapMode: Text.WordWrap
                renderType: Text.NativeRendering
                font.pointSize: 12
            }

            Text {
                id: getStarted
                text: qsTr("Getting Started")
                anchors.top: whatIsPireal.bottom
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.topMargin: 50
                renderType: Text.NativeRendering
                font.pointSize: 18
            }
            ColumnLayout {
                id: buttons
                spacing: 10
                anchors.top: getStarted.bottom
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.topMargin: 30

                Button {
                    text: qsTr("Create a new Database")

                }

                Button {
                    text: qsTr("Open a Database")
                    implicitWidth: parent.width
                }


            }



            Rectangle {
                id: separator
                color: "#ccc"
                width: 1
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                anchors.topMargin: 20
                anchors.bottomMargin: 20
                anchors.left: parent.right

            }


        }

        Item {
            id: rightArea

            Layout.fillWidth: true
            Layout.fillHeight: true

            Button {
                text: "?"
                bold: true
                fontSize: 12
                width: 30; height: 30
                radiuss: width / 2
                anchors {
                    right: parent.right
                    top: parent.top
                    margins: 10
                }

                onClicked: {
                    flipArea.flipped = !flipArea.flipped;
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
                            color: listItem.current ? "#4896b8" : "#ebebeb"
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
                                ColorAnimation {}
                            }

                            Column {
                                spacing: 8
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
                                    renderType: Text.NativeRendering
                                }

                                Text {
                                    text: path
                                    color:listItem.current ? "#fafbfb" : "#979dac"
                                    width: parent.width
                                    elide: Text.ElideLeft
                                    renderType: Text.NativeRendering
                                    font.pixelSize: 16
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
                            anchors {
                                left: parent.left
                                right: parent.right
                                top: parent.top
                                margins: 20
                            }

                            Text {
                                color: "#4896b8"
                                font.pointSize: 22
                                font.bold: true
                                text: qsTr("¿What's is Pireal?")
                                renderType: Text.NativeRendering
                            }

                            Text {
                                color: "gray"
                                font.pointSize: 12
                                text: qsTr("<b>π</b>real is a teaching tool for use in learning introduction to database. It allows the user to interactively experiment with Relational Algebra.\n")
                                width: parent.width
                                wrapMode: Text.WordWrap
                                renderType: Text.NativeRendering
                            }
                        }
                    }
                }
            }

            Text {
                id: title

                text: qsTr("Recents Database")
                color: "#838b8c"
                font.pixelSize: 18
                renderType: Text.NativeRendering
                anchors.left: flipArea.left
                anchors.bottom: flipArea.top
                anchors.bottomMargin: 10
                visible: !flipArea.flipped
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
         color: "#838b8c"
         height: logoPython.height
         verticalAlignment: Text.AlignVCenter
         font.pixelSize: 12
        }

        Image { id: logoPython; source: "python-logo.png"; opacity: 0.7 }
        Image { source: "bwqt.png"; opacity: 0.7 }
    }

    Text {
        text: "Copyright © 2015-" + new Date().getFullYear() + " Gabriel Acosta. Pireal is distributed under the terms of the GNU GPLv3+ copyleft license"
        color: "#838b8c"
        anchors {
            bottom: parent.bottom
            left: parent.left
            bottomMargin: 5
            leftMargin: 10
        }
        font.pixelSize: 12
        visible: root.compressed ? false : true
        renderType: Text.NativeRendering
    }

}
