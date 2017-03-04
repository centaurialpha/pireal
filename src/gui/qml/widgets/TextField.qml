import QtQuick 2.6
import QtQuick.Controls 2.0

TextField {
    id: root

    property bool hasError: false
    renderType: Text.NativeRendering
    width: parent.width
    background: Rectangle {
        implicitHeight: 40
        border.color: root.hasError ? "#e3757e" : (root.focus ? "#4896b8" : "#ccc")
        border.width: root.focus ? 2 : 1
    }

}
