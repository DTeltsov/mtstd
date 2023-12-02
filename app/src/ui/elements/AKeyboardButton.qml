import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3
import QtQuick.Controls.Material 2.1

import "qrc:/AColor.js" as Colors

Item {
    id: main
    signal keypress(string key)
    width: 26
    height: 34
    property string text: ""
    property string text_alt: ""
    property string color: Colors.dark_1
    property bool alt_mode: false

    FontLoader { id: roboto; source: "qrc:/fonts/robotoRegular.ttf" }

    Rectangle {
        color: Colors.black
        radius: 3.7
        width: main.width
        height: main.height
    }

    Rectangle {
        id: btn
        color: main.color
        radius: 3.7
        width: main.width
        height: main.height - 2

        Text {
            id: caption
            text: main.alt_mode ? main.text_alt : main.text
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.verticalCenter: parent.verticalCenter
            font.pixelSize: 18
            font.family: roboto.name
            color: Colors.white
        }

        MouseArea {
            anchors.fill: parent
            onClicked: {
                main.keypress(caption.text)
                clickAnimation.running = true
            }
        }
    }

    SequentialAnimation {
        id: clickAnimation
        running: false

        ParallelAnimation {
            NumberAnimation { target: btn; property: "height"; to: 34; duration: 100 }
            ColorAnimation { target: btn; property: "color"; to: Colors.middle_4; duration: 100 }
        }

        ParallelAnimation {
            NumberAnimation { target: btn; property: "height"; to: 32; duration: 100 }
            ColorAnimation { target: btn; property: "color"; to: btn.color; duration: 100 }
        }
    }
}
