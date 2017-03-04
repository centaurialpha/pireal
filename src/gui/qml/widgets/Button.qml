import QtQuick 2.3
import QtQuick.Controls 1.0
import QtQuick.Controls.Styles 1.0

Button {
    id: button
    scale: pressed ? 0.9 : 1
    property bool bold: false
    property int fontSize: 12
    property int radiuss: 0
    property bool error: false

    style: ButtonStyle {
        background: Item {
            anchors.fill: parent
            implicitHeight: 40
            Rectangle {
                anchors.fill: parent
                color: (button.checked || button.pressed)
                       ? "#4896b8": (button.hovered ? (error ? "#e3757e": "#4896b8") : "white")
                border.width: 1
                border.color: "#4896b8"
                radius: radiuss

                Behavior on color {
                    ColorAnimation {}
                }
            }
        }

        label: Text {
            id: txt
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            text: button.text
            smooth: true
            color: button.hovered ? "white" : "#838b8c"
            font.bold: bold
            font.pointSize: fontSize
            renderType: Text.NativeRendering
        }
    }
    function he() {
        console.debug(txt.height);
    }
}
