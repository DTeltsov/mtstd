import QtQuick 2.7
import QtQuick.Controls 2.3

import "qrc:/AColor.js" as Colors


Popup {
    id: root
    y: parent.height - height
    x: (parent.width - width) / 2
    implicitWidth: toolTipText.paintedWidth + 20
    implicitHeight: toolTipText.paintedHeight + 10

    padding: 0
    margins: 0
    closePolicy: Popup.NoAutoClose

    property alias text: toolTipText.text
    readonly property alias animDestroy: animDestroy
    readonly property alias mouseArea: mouseArea
    signal finished

    background: Rectangle {
        color: Colors.middle_4
        radius: 3
        border {
            width: 1
            color: Colors.light_4
        }
    }
    Text {
        id: toolTipText
        anchors.centerIn: parent
        color: Colors.light_4
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        font.family: ajaxFont.name
    }

    SequentialAnimation {
        id: animDestroy
        property var pauseSeconds: 0.9
        running: false
        NumberAnimation { target: root; property: "opacity"; to: 1 }
        PauseAnimation { duration: animDestroy.pauseSeconds * 100 }
        NumberAnimation { target: root; duration: 500; property: "opacity"; to: 0 }

        onStarted: {
            root.open()
        }
        onStopped: {
            if (root.opacity == 0) {
                // animDestroy.finished is allowed only starting with QtQuick 2.12
                root.finished()
            }
        }
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: true

        onEntered: {
            root.opacity = 1
            animDestroy.stop()
        }
    }
}