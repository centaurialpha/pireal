import QtQuick 2.7

TextField {
    id: root

    property bool hasError: false
    property string borderColor: hasError ? "#e3757e" : (focus ? "#4896b8" : "#ccc");

    renderType: Text.NativeRendering
    width: parent.width
    background: Rectangle {
        implicitHeight: 40
        border.color: borderColor;
        border.width: root.focus ? 2 : 1
    }

}
