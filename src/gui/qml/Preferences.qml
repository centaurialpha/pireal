import QtQuick 2.5
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.1

Item {
    id: root

    signal close();
    signal resetSettings();
    signal checkForUpdates();
    signal changeLanguage(string lang);
    signal stateCurrentLineChanged(bool state);
    signal stateMatchingParenChanged(bool state);
    signal needChangeFont();

    function checkForUpdate() {
        root.enabled = false
        busy.visible = true;
        checkForUpdates();
    }

    function threadFinished() {
        busy.visible = false;
        root.enabled = true;
    }

    function addLangsToCombo(languages) {
        comboLangs.model = languages;
    }

    function setCurrentLanguage(lang) {
        var index = comboLangs.find(lang);
        comboLangs.currentIndex = index;
    }

    function setFontFamily(font, currentSize) {
        var btnText = font + ', ' + currentSize
        fontBtn.text = btnText;
    }

    function setInitialStates(curLineState, matchParenState) {
        currentLineCheck.checked = curLineState ? Qt.Checked : Qt.Unchecked;
        matchParenCheck.checked = matchParenState ? Qt.Checked : Qt.Unchecked;
    }

    GroupBox {
        id: container
        font.pointSize: 16
        width: parent.width / 2.5
        anchors {
            top: parent.top
            horizontalCenter: parent.horizontalCenter
            topMargin: parent.width / 9
        }

        ColumnLayout {
            spacing: 20
            anchors.fill: parent
            Button {
                text: qsTr("Check for updates")
                anchors.right: parent.right
                anchors.left: parent.left
                onClicked: {
                    checkForUpdate();
                }
            }

            Row {
                spacing: 20

                Switch {
                    id: currentLineCheck
                    text: qsTr("Highlight Current Line")
                    font.pointSize: 10
                    onCheckedChanged: {
                        stateCurrentLineChanged(checked);
                    }
                }

                Switch {
                    id: matchParenCheck
                    text: qsTr("Matching Parenthesis")
                    font.pointSize: 10
                    onCheckedChanged: {
                        stateMatchingParenChanged(checked);
                    }
                }
            }

            Button {
                id: fontBtn
                text: ""
                anchors.right: parent.right
                anchors.left: parent.left
                onClicked: {
                    // Emito la señal para mostrar el QFontDialog
                    needChangeFont();
                }
            }

            Column {
                spacing: 10
                anchors.bottom: parent.bottom
                anchors.left: parent.left
                anchors.right: parent.right
                ComboBox {
                    id: comboLangs
                    font.pointSize: 14
                    anchors.right: parent.right
                    anchors.left: parent.left
                    onActivated: {
                        var langText = textAt(index);
                        // Emito la señal
                        changeLanguage(langText);
                    }
                }
                Label {
                    text: qsTr("(Requires restart Pireal)");
                    renderType: Text.NativeRendering
                    font.pointSize: 10
                }
            }


        }
    }

    // Botones
    Row {
        spacing: 20
        anchors {
            bottom: parent.bottom
            right: parent.right
            margins: 20
        }

        Button {
            text: qsTr("Back");
            onClicked: {
                root.close();
            }
        }

        Button {
            text: qsTr("Reset Configurations");
            onClicked: {
                root.resetSettings();
            }
        }
    }

    Rectangle {
        id: busy
        anchors.fill: parent
        color: "white"
        opacity: 0.8
        visible: false

        BusyIndicator {
            id: control
            anchors.centerIn: parent

            contentItem: Item {
                implicitWidth: 64
                implicitHeight: 64

                Item {
                    id: item
                    x: parent.width / 2 - 32
                    y: parent.height / 2 - 32
                    width: 64; height: 64
                    opacity: control.running ? 1 : 0

                    Behavior on opacity {
                        OpacityAnimator { duration: 250 }
                    }

                    RotationAnimator {
                        target: item
                        running: control.visible && control.running
                        from: 0
                        to: 360
                        loops: Animation.Infinite
                        duration: 1250
                    }
                    Repeater {
                        id: repeater
                        model: 6

                        Rectangle {
                            x: item.width / 2 - width / 2
                            y: item.height / 2 - height / 2
                            implicitHeight: 10
                            implicitWidth: 10
                            radius: 5
                            color: "#4896b8"
                            transform: [
                                Translate {
                                    y: -Math.min(item.width, item.height) * .5 + 5
                                },
                                Rotation {
                                    angle: index / repeater.count * 360
                                    origin.x: 5; origin.y: 5
                                }

                            ]
                        }
                    }
                }
            }
        }
    }
}
