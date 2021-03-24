import QtQuick 2.6
import "widgets"
import "logic.js" as Logic

Rectangle {
    id: root

    width: 550; height: 300
    border.width: 1
    border.color: "#a0a0a0"

    signal close;
    signal databaseNameChanged(string dbName);
    signal locationChanged();
    signal create(string dbName, string location, string fname);

    // Área de título
    Item {
        id: titleArea
        anchors.fill: parent

        Rectangle {
            id: separator

            color: "#e8e8e8"
            anchors {
                top: parent.top
                left: parent.left
                right: parent.right
                topMargin: title.height
                leftMargin: 20
                rightMargin: 20
            }
            width: parent.width
            height: 1
        }

        Text {
            id: title
            text: qsTr("New Database");
            font.pointSize: 22
            color: "#838b8c"
            renderType: Text.NativeRendering
            anchors {
                top: parent.top
                horizontalCenter: parent.horizontalCenter
            }
        }
    }

    // Formulario
    Column {
        spacing: 10

        anchors {
            left: parent.left
            right: parent.right
            leftMargin: 30
            rightMargin: 30
            verticalCenter: parent.verticalCenter
        }

        TextField {
            id: databaseName
            focus: true
            //Layout.fillWidth: true
            placeholderText: qsTr("Database Name");
            onTextChanged: {
                hasError = false;
                // Emito la señal
                databaseNameChanged(text);
            }
        }

        Row {
            spacing: 0

            TextField {
                id: dbLocation
                //Layout.fillWidth: true
                readOnly: true
            }
            Button {
                texto: "..."
                implicitWidth: 30
                onClicked: { locationChanged(); }
            }
        }

        TextField {
            id: dbFilename
            readOnly: true
            //Layout.fillWidth: true
        }

    }

    // Botones
    Row {
        spacing: 10
        anchors {
            bottom: parent.bottom
            right: parent.right
            margins: 10
        }

        Button {
            texto: qsTr("Create")
            height: 30
            onClicked: { Logic.onButtonSaveClicked(); }
        }

        Button {
            texto: qsTr("Cancel")
            height: 30
            onClicked: {
                close();
            }
        }
    }


    function setFilename(fname) {
        dbFilename.text = fname;
    }

    function setFolder(folder) {
        dbLocation.text = folder;
    }

    function dbName() {
        return databaseName.text;
    }

}
