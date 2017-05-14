import QtQuick 2.3
import QtQuick.Controls 2.0
import QtQuick.Controls.Styles 1.0

Button {
    id: button

    contentItem: Text {
        text: button.text
        verticalAlignment: Text.AlignVCenter
        horizontalAlignment: Text.AlignHCenter
        renderType: Text.NativeRendering
        color: "#484c4d"
    }

}
