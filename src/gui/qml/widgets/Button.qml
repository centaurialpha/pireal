import QtQuick 2.3
import QtQuick.Controls 1.0
import QtQuick.Controls.Styles 1.0

Button {
    id: button
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
                       ? ( error ? Qt.darker("#e3757e", 1.5) :
                                   Qt.darker("#4896b8", 1.5)) :
                         (button.hovered ? (error ? "#e3757e": "#4896b8") : "white")
                border.width: 1
                border.color: "#4896b8"
                radius: radiuss


                Behavior on color {
                    ColorAnimation { duration: 70 }
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
}
