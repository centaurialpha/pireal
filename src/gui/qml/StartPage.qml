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
import QtQuick 2.5
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
        text: "Click en <b>Nueva</b>, <b>Obrir</b> o <b>Ejemplo</b> para comenzar!"
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
            texto: "Nueva"
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
            texto: "Abrir"
            z: 1
            CustomBorder {
                commonBorder: true
                borderColor: "#c4c7ca"
            }
            onClicked: root.openDatabase();
        }
        Button {
            texto: "Ejemplo"
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
                text: qsTr("Base de Datos Recientes")
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

    //    property bool widthCompressed: false
    //    property bool heightCompressed: false

    //    onWidthChanged: {
    //        if(width < 925) {
    //            widthCompressed = true;
    //        } else {
    //            widthCompressed = false;
    //        }
    //    }

    //    onHeightChanged: {
    //        if(height < 580) {
    //            heightCompressed = true;
    //        } else {
    //            heightCompressed = false;
    //        }
    //    }

    //    function loadItem(name, path) {
    //        listModel.append({"name": name, "path": path})
    //    }

    //    function clear() {
    //        listModel.clear();
    //    }

    //    ListModel {
    //        id: listModel

    //        ListElement {
    //            name: ""
    //            path: ""
    //        }
    //    }

    //    Component.onCompleted: {
    //        listModel.clear();
    //    }



    //    Column {
    //        id: leftArea
    //        anchors.top: parent.top
    //        anchors.left: parent.left
    //        anchors.leftMargin: 10
    //        width: 410
    //        spacing: 30

    //        Image {
    //            id: logo
    //            source: "pireal_logo-black.png"
    //            anchors.horizontalCenter: parent.horizontalCenter
    //        }

    //        Text {
    //            id: whatIsPireal
    //            text: qsTr("<b>Pireal</b> is a teaching tool for use in learning introduction to database. It allows the user to interactively experiment with Relational Algebra.")
    //            anchors {
    //                left: parent.left
    //                right: parent.right
    //                rightMargin: 1
    //            }
    //            wrapMode: Text.Wrap
    //            renderType: Text.NativeRendering
    //            font.pointSize: 12
    //            color: "#5f6566"

    //        }

    //        Text {
    //            id: getStarted
    //            text: qsTr("Getting Started")
    //            anchors.horizontalCenter: parent.horizontalCenter
    //            renderType: Text.NativeRendering
    //            font.pointSize: 18
    //            color: "#5f6566"
    //        }

    //        Row {
    //            id: buttons
    //            spacing: 5
    //            anchors.horizontalCenter: parent.horizontalCenter
    //            Button {
    //                texto: qsTr("Create a new Database")
    //                onClicked: {
    //                    newDatabase();
    //               }
    //            }

    //            Button {
    //                texto: qsTr("Open a Database")
    //                //implicitWidth: parent.width;
    //                onClicked: {
    //                    openDatabase();
    //                }
    //            }
    //        }

    //        Column {
    //            spacing: 10
    //            //anchors.top: buttons.bottom
    //            anchors.left: parent.left
    //            anchors.right: parent.right
    //            anchors.margins: 30

    //            Text {
    //                text: qsTr("- Open a recent database from the list.")
    //                font.pointSize: 12
    //                renderType: Text.NativeRendering
    //                anchors.left: parent.left
    //                anchors.right: parent.right
    //                wrapMode: Text.WordWrap
    //                color: "#5f6566"
    //            }

    //            Text {
    //                text: qsTr("- Change the language from the <a href=\"#\">Preferences</a>.")
    //                anchors.left: parent.left
    //                anchors.right: parent.right
    //                font.pointSize: 12
    //                renderType: Text.NativeRendering
    //                linkColor: "#4896b8"
    //                color: "#5f6566"
    //                wrapMode: Text.WordWrap
    //                onLinkActivated: {
    //                    openPreferences();
    //                }
    //            }

    //            Text {
    //                text: qsTr("- Open a full <a href=\"#\">example</a>.")
    //                anchors.left: parent.left
    //                anchors.right: parent.right
    //                font.pointSize: 12
    //                renderType: Text.NativeRendering
    //                linkColor: "#4896b8"
    //                color: "#5f6566"
    //                wrapMode: Text.WordWrap
    //                onLinkActivated: {
    //                    openExample();
    //                }
    //            }
    //        }

    //        Text {

    //            text: qsTr("<b>Pireal</b> is Free Software and is mainly developed in
    //                       <a href=\"http://python.org\">Python</a> and <a
    //                       href=\"http://qt.io\">Qt/QML</a>, so if you want to collaborate,
    //                       suggest something or just study it, the source code is available
    //                       <a href=\"http://github.com/centaurialpha/pireal\">here</a>.")
    //            anchors.left: parent.left
    //            anchors.right: parent.right

    //            wrapMode: Text.WordWrap
    //            color: "#5f6566"
    //            linkColor: "#4896b8"
    //            visible: !heightCompressed
    //            onLinkActivated: {
    //                Qt.openUrlExternally(link)
    //            }
    //        }

    //    }


    //    Rectangle {
    //        id: separator
    //        color: "#ccc"
    //        width: 1
    //        anchors.top: parent.top
    //        anchors.topMargin: 20
    //        anchors.bottom: parent.bottom
    //        anchors.bottomMargin: 20
    //        anchors.left: leftArea.right
    //    }

    //    Item {
    //        id: rightArea

    //        anchors.left: separator.right
    //        anchors.right: parent.right
    //        anchors.top: parent.top
    //        anchors.bottom: parent.bottom

    //        Rectangle {
    //            id: container

    //            width: root.width / 2; height: root.height / 1.5
    //            anchors.centerIn: parent
    //            color: "#f5f5f5"
    //            border.color: "#dddddd"
    //            border.width: 1
    //            enabled: !parent.flipped
    //            radius: 3
    //            Text {
    //                text: qsTr("No recent database")
    //                color: "#838b8c"
    //                anchors.centerIn: parent
    //                visible: listModel.count ? false : true
    //                font.pointSize: 20
    //                renderType: Text.NativeRendering
    //            }
    //            ListView {
    //                id: listView

    //                anchors {
    //                    topMargin: 5
    //                    fill: parent
    //                }
    //                width: parent.width / 2.5; height: parent.height / 1.5
    //                model: listModel
    //                spacing: 3
    //                focus: true
    //                clip: true
    //                currentIndex: -1
    //                property bool empty: listView.count == 0
    //                delegate: Rectangle {
    //                    id: listItem
    //                    anchors {
    //                        left: parent.left
    //                        right: parent.right
    //                        leftMargin: 5
    //                        rightMargin: 5
    //                    }
    //                    height: 75
    //                    property bool current: ListView.isCurrentItem
    //                    color: listItem.current ? "#5294e2" : "#ebebeb"
    //                    MouseArea {
    //                        anchors.fill: parent
    //                        hoverEnabled: true

    //                        onHoveredChanged: {
    //                            listView.currentIndex = index;
    //                        }

    //                        onExited: {
    //                            listView.currentIndex = -1;
    //                        }

    //                        onClicked: {
    //                            root.openRecentDatabase(path);
    //                        }
    //                    }

    //                    Column {
    //                        spacing: 8
    //                        anchors {
    //                            verticalCenter: parent.verticalCenter
    //                            left: parent.left
    //                            right: parent.right
    //                            leftMargin: 20
    //                            rightMargin: 20
    //                        }

    //                        Text {
    //                            text: name
    //                            font.bold: true
    //                            font.pixelSize: 30
    //                            color: listItem.current ? "#fafbfb" : "#979dac"
    //                            renderType: Text.NativeRendering
    //                        }

    //                        Text {
    //                            text: path
    //                            color:listItem.current ? "#fafbfb" : "#979dac"
    //                            width: parent.width
    //                            elide: Text.ElideLeft
    //                            renderType: Text.NativeRendering
    //                            font.pixelSize: 16
    //                        }
    //                    }

    //                    Image {
    //                        id: imgDelete
    //                        source: "close.png"
    //                        anchors {
    //                            right: parent.right
    //                            top: parent.top
    //                            topMargin: 15
    //                            rightMargin: 15
    //                        }
    //                        scale: ma.pressed ? 0.7 : 1
    //                        visible: listItem.current ? true: false
    //                        onVisibleChanged: NumberAnimation {
    //                            target: imgDelete; property: "scale"; from: 0; to: 1; duration: 200
    //                        }

    //                        MouseArea {
    //                            id: ma
    //                            anchors.fill: parent
    //                            onClicked: {
    //                                root.removeCurrent(path);
    //                                listView.model.remove(index);
    //                            }
    //                        }
    //                    }
    //                }
    //            }
    //        }
    //    }

    //    Row {
    //        spacing: 10
    //        anchors {
    //            bottom: parent.bottom
    //            right: parent.right
    //            bottomMargin: 5
    //            rightMargin: 10
    //        }

    //        Text {
    //         text: "Powered by: "
    //         color: "#838b8c"
    //         height: logoPython.height
    //         verticalAlignment: Text.AlignVCenter
    //         font.pixelSize: 12
    //        }

    //        Image { id: logoPython; source: "python-logo.png"; opacity: 0.7 }
    //        Image { source: "bwqt.png"; opacity: 0.7 }
    //    }

    //    Text {
    //        text: "Copyright © 2015-" + new Date().getFullYear() + " Gabriel Acosta. Pireal is distributed under the terms of the GNU GPLv3+ copyleft license"
    //        color: "#838b8c"
    //        anchors {
    //            bottom: parent.bottom
    //            left: parent.left
    //            bottomMargin: 5
    //            leftMargin: 10
    //        }
    //        font.pixelSize: 12
    //        renderType: Text.NativeRendering
    //        visible: !widthCompressed
    //    }

}
