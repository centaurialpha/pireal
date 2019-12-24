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

    SystemPalette { id: palette; colorGroup: SystemPalette.Active }

    color: palette.base

    signal openRecentDatabase(string path)
    signal openPreferences();
    signal openExample
    signal newDatabase
    signal openDatabase
    signal removeItem(int index);

    Item {
        id: mainContainer
        anchors.fill: parent
        anchors.leftMargin: 250
        anchors.rightMargin: 250
        anchors.topMargin: 150
        anchors.bottomMargin: 150

        Item {
            id: topContainer
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.right: parent.right
            height: parent.height / 6
            Text {
                id: title
                text: "<b>π</b>real"
                color: palette.text
                font.pointSize: 32
            }
            Text {
                id: subTitle
                text: "free and open source Relational Algebra Interpreter"
                color: palette.mid
                font.pointSize: 14
                anchors.top: title.bottom
            }
        }
        Item {
            id: leftContainer
            anchors.top: topContainer.bottom
            anchors.left: mainContainer.left
            anchors.bottom: mainContainer.bottom
            width: mainContainer.width / 2

            Text {
                id: txtStarted
                text: "Get started!"
                color: palette.text
                font.pointSize: 18
            }
            Row {
                id: boxButtons
                anchors.top: txtStarted.bottom
                anchors.topMargin: 10
                spacing: -3


                Button {
                    texto: qsTr("New Database")
                    textColor: palette.buttonText
                    radius: 3
                    color: palette.alternateBase
                    CustomBorder {
                        commonBorder: false
                        borderColor: palette.shadow
                        radius: 3
                    }

                    onClicked: root.newDatabase();
                }
                Button{
                    texto: qsTr("Open Database")
                    textColor: palette.buttonText
                    color: palette.alternateBase
                    z: 1
                    CustomBorder {
                        commonBorder: true
                        borderColor: palette.shadow
                    }
                    onClicked: root.openDatabase();
                }
                Button {
                    texto: qsTr("Example")
                    textColor: palette.buttonText
                    radius: 3
                    color: palette.alternateBase
                    CustomBorder {
                        commonBorder: false
                        borderColor: palette.shadow
                        radius: 3
                    }
                    onClicked: root.openExample()
                }
            }
            Text {
                id: txtLearn
                color: palette.text
                text: qsTr("Learn")
                font.pointSize: 18
                anchors.top: boxButtons.bottom
                anchors.left: parent.left
                anchors.topMargin: 50
            }
            Column {
                id: learnItems
                anchors.top: txtLearn.bottom
                anchors.left: parent.left
                anchors.topMargin: 10
                width: leftContainer.width
                spacing: 10

                HelpItem {
                    title: qsTr("Be a hacker!")
                    link: "#"
                    description: "Learn how you can collaborate with the Pireal source code"
                    width: parent.width - 30
                }
                HelpItem {
                    title: qsTr("How was Pireal programmed?")
                    link: "#"
                    description: "Pireal has its own interpreter that was built from scratch!"
                    width: parent.width - 30
                }
                HelpItem {
                    title: qsTr("Fun facts")
                    link: "#"
                    description: "¿How many lines of code does Pireal have? ¿How much development time has been dedicated? You can see the answers to these questions here"
                    width: parent.width - 30
                }
            }
            Text {
                id: txtHelp
                text: qsTr("Help")
                color: palette.text
                font.pointSize: 18
                anchors.top: learnItems.bottom
                anchors.left: parent.left
                anchors.topMargin: 50
            }
            Column {
                spacing: 1
                anchors.top: txtHelp.bottom
                anchors.left: parent.left
                anchors.topMargin: 10
                Link {
                    title: qsTr("Tutorial")
                    link: "#"
                }
                Link {
                    title: qsTr("Issue Tracker")
                    link: "http://github.com/centaurialpha/pireal/issues"
                }
                Link {
                    title: qsTr("Web Page")
                    link: "http://centaurialpha.github.io/pireal"
                }
                Link {
                    title: qsTr("User Guide")
                    link: "#"
                }

            }
        }
        Item {
            id: rightContainer

            width: mainContainer.width / 2
            anchors.right: mainContainer.right
            anchors.bottom: mainContainer.bottom
            anchors.top: topContainer.bottom

            Text {
                id: txtRecentsDb
                text: "Recent Databases"
                color: palette.text
                font.pointSize: 18
            }

            Rectangle {
                anchors {
                    top: txtRecentsDb.bottom
                    bottom: parent.bottom
                    right: parent.right
                    left: parent.left
                    topMargin: 20
                }
                color: palette.alternateBase

                ListView {
                    id: listView

                    anchors.fill: parent
                    anchors.margins: 20
                    clip: true
                    focus: true
                    spacing: 10
                    model: listModel

                    delegate: Rectangle {
                        id: listItem
                        color: palette.highlight
                        height: 40
                        radius: 1
//                        width: parent.width
                        anchors.left: parent.left
                        anchors.right: parent.right
                        property bool current: ListView.isCurrentItem

                        MouseArea {
                            anchors.fill: listItem
                            hoverEnabled: true
                            cursorShape: containsMouse ? Qt.PointingHandCursor : Qt.ArrowCursor

                            onClicked: {
                                path = listView.model.get_path(index)
                                openRecentDatabase(path)
                            }
                        }
                        SequentialAnimation {
                            id: closeAnimation
                            PropertyAction { target: listItem; property: "ListView.delayRemove"; value: true }
                            NumberAnimation { target: listItem; property: "scale"; to: 0; duration: 250; easing.type: Easing.InOutQuad }
                            PropertyAction { target: listItem; property: "ListView.delayRemove"; value: false }
                        }

                        Row {
                            spacing: 10
                            anchors.fill: parent
                            anchors.margins: 10
                            Text {
                                id: txtDisplayName
                                text: displayName
                                color: palette.buttonText
                                font.pointSize: 14
                                anchors.bottom: parent.bottom
                            }
                            Text {
                                text: path
                                color: palette.mid
                                font.pointSize: 10
                                width: parent.width - txtDisplayName.width - parent.spacing - imgClose.width - 3
                                elide: Text.ElideMiddle
                            }
                        }
                        Image {
                            id: imgClose
                            source: "close.png"
                            anchors {
                                right: parent.right
                                top: parent.top
                                topMargin: 10
                                rightMargin: 10
                            }
                            MouseArea {
                                anchors.fill: imgClose
                                onClicked: {
                                    root.removeItem(index)
                                    closeAnimation.start()
                                }
                            }
                        }
                    }
                }
            }
        }

    }

    Row {
        id: rrow
        spacing: 10
        anchors {
            bottom: parent.bottom
            right: parent.right
            bottomMargin: 5
            rightMargin: 10
        }

        Text {
            text: "Powered by: "
            color: palette.text
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
        color: palette.text
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
