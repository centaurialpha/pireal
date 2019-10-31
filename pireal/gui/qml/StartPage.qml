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
import QtQuick 2.7
import "widgets"


Rectangle {
    id: root

    color: "#ffffff"

    signal openRecentDatabase(string path)
    signal openPreferences();
    signal openExample
    signal newDatabase
    signal openDatabase
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

    Image {
        id: logo
        source: "pireal_logo.png"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.topMargin: 90
    }
    Text {
        id: textoWelcome
        text: qsTr("Click in <b>New</b>, <b>Open</b> or <b>Example</b> to get started!")
        anchors.top: logo.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.topMargin: 10
        renderType: Text.NativeRendering
    }

    Row {
        id: buttons
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: textoWelcome.bottom
        anchors.topMargin: 10
        spacing: -3


        Button {
            texto: qsTr("New")
            radius: 3
            CustomBorder {
                commonBorder: false
                borderColor: "#c4c7ca"
                lBorderwidth: 1
                radius: 3
            }

            onClicked: root.newDatabase();
        }
        Button{
            texto: qsTr("Open")
            z: 1
            CustomBorder {
                commonBorder: true
                borderColor: "#c4c7ca"
            }
            onClicked: root.openDatabase();
        }
        Button {
            texto: qsTr("Example")
            radius: 3
            CustomBorder {
                commonBorder: false
                borderColor: "#c4c7ca"
                rBorderwidth: 1
                lBorderwidth: 1
                radius: 3
            }
            onClicked: root.openExample()
        }
    }

    Rectangle {

        id: listContainer
        color: "#c9cccf"
        radius: 3
        border.color: "#ccc"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: buttons.bottom
        anchors.topMargin: 20
        height: 300
        width: 600

        Rectangle {
            id: title

            height: 35
            color: "#e9ebec"
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.margins: 8
            Text {
                text: qsTr("Recent Databases")
                font.bold: true
                font.italic: true
                color: "#303336"
                font.pixelSize: 20
                anchors.centerIn: parent
                renderType: Text.NativeRendering
            }
        }

        Rectangle {

            color: "#c9cccf"
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.top: title.bottom
            anchors.margins: 8

            ListView {
                id: listView

                anchors.fill: parent
                clip: true
                focus: true
                spacing: 7

                model: listModel
                delegate: Rectangle {
                    id: listItem
                    color: "#f4f5f5"
                    height: 60
                    radius: 3
                    anchors {
                        left: parent.left
                        right: parent.right
                    }
                    property bool current: ListView.isCurrentItem
                    MouseArea {
                        anchors.fill: parent
                        hoverEnabled: true
                        cursorShape: containsMouse ? Qt.PointingHandCursor : Qt.ArrowCursor

                        onClicked: root.openRecentDatabase(path);

                    }
                    SequentialAnimation {
                        id: closeAnimation
                        PropertyAction { target: listItem; property: "ListView.delayRemove"; value: true }
                        NumberAnimation { target: listItem; property: "scale"; to: 0; duration: 250; easing.type: Easing.InOutQuad }
                        PropertyAction { target: listItem; property: "ListView.delayRemove"; value: false }
                    }

                    Column {

                        anchors.bottom: parent.bottom
                        anchors.left: parent.left
                        anchors.right: parent.right
                        anchors.leftMargin: 20
                        anchors.bottomMargin: 10
                        anchors.top: parent.top
                        anchors.topMargin: 10
                        Text {
                            color: "#555"
                            font.bold: true
                            font.pixelSize: 18
                            text: name
                            renderType: Text.NativeRendering
                        }
                        Text {
                            color: "#555"
                            text: path
                            width: parent.width
                            elide: Text.ElideLeft
                            renderType: Text.NativeRendering
                        }
                    }

                    Image {
                        source: "close.png"
                        anchors {
                            right: parent.right
                            top: parent.top
                            topMargin: 10
                            rightMargin: 10
                        }
                        scale: ma.pressed ? 0.7 : 1
                        MouseArea {
                            id: ma
                            anchors.fill: parent

                            onClicked: {
                                root.removeCurrent(path);
                                listView.model.remove(index);
                                closeAnimation.start();
                            }
                        }
                    }
                }

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
            color: "#444"
            height: logoPython.height
            verticalAlignment: Text.AlignVCenter
            font.pixelSize: 12
            renderType: Text.NativeRendering
        }

        Image { id: logoPython; source: "python-logo.png"; opacity: 0.7 }
        Image { source: "bwqt.png"; opacity: 0.7 }
    }

    Text {
        text: "Copyright © 2015-" + new Date().getFullYear() + " Gabriel Acosta. Pireal is distributed under the terms of the GNU GPLv3+ copyleft license"
        color: "#444"
        renderType: Text.NativeRendering
        anchors {
            bottom: parent.bottom
            left: parent.left
            bottomMargin: 5
            leftMargin: 10
        }
        font.pixelSize: 12
    }
}