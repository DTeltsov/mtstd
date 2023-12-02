import QtQuick 2.3
import QtQuick.Controls.Styles 1.4
import QtQuick.Controls 1.4
import "qrc:/AColor.js" as Colors


ProgressBar {
    value: 0
    width: 80
    height: width
    minimumValue: 0
    maximumValue: 30

    property var elapsed: Math.round(value * maximumValue)
    property alias progressTimer: progressTimer

    signal timeout

    function compileText() {
        return elapsed
    }

    Timer {
        id: progressTimer
        interval: 100
        repeat: true
        onTriggered: {
            parent.value += interval / (maximumValue * 1000)
            if (elapsed > parent.maximumValue) {
                parent.value = 1
                // stop timer
                progressTimer.stop()
                // emit signal
                parent.timeout()
            }
        }
    }
    onVisibleChanged: {
        value = 0
        if (visible){
            progressTimer.start()
        } else {
            progressTimer.stop()
        }
    }

    style: ProgressBarStyle {
        panel : Rectangle {
            color: "transparent"
            implicitWidth: control.width
            implicitHeight: implicitWidth

            Rectangle {
                id: innerRing
                z: 1
                anchors.fill: parent
                radius: Math.max(width, height) / 2
                color: "transparent"
                border.color: Colors.middle_3
                border.width: 3
            }

            Text {
                anchors.centerIn: parent
                color: Colors.green_1
                font.pixelSize: Math.floor(control.width / 3.33)
                text: compileText()
            }
        }
    }
}