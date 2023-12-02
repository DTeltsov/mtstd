import QtQuick 2.7
import QtQuick.Controls 2.3

import "qrc:/AColor.js" as Colors


Button {
    id: btn
    implicitWidth: 100
    implicitHeight: 40

    text: "Button"
    activeFocusOnTab: true
    property string colorText: Colors.black
    property color colorBtn: Colors.green_2
    property alias cursorShape: mouseArea.cursorShape
    property alias back: back
    property alias item: item

    contentItem: Text {
        id: item
        anchors.centerIn: parent
        text: btn.text
        color: btn.enabled ? btn.colorText : Colors.light_4
        opacity: btn.enabled ? 1 : 0.8
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        elide: Text.ElideRight
    }

    background: Rectangle {
        id: back
        radius: 40
        color: btn.enabled ? btn.colorBtn : Colors.middle_4
        border {
            width: btn.enabled ? 0 : 1
            color: Colors.middle_3
        }
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        onPressed: mouse.accepted = false
        cursorShape: enabled ? Qt.PointingHandCursor : Qt.ArrowCursor
    }
}
