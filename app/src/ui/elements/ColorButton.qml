import QtQuick 2.7
import QtQuick.Controls 2.3

import "qrc:/AColor.js" as Colors
import "qrc:/theme"


Button {
    id: root
    implicitWidth: 100
    implicitHeight: 40
    text: "colorButton"
    activeFocusOnTab: false

    property string color: Colors.red_1
    property string extraColor: Colors.black
    property bool selected: false
    property bool active: false
    property alias cursorShape: mouseArea.cursorShape
    property alias back: back
    property alias item: item
    property alias mouseArea: mouseArea

    contentItem: Text {
        id: item
        anchors.centerIn: parent
        width: root.width
        text: root.text
        color: (!root.selected && !root.active ? root.color : root.extraColor)
        Behavior on color { ColorAnimation { duration: 300 } }

        elide: Text.ElideRight
        mouseArea.enabled: false
    }

    background: Rectangle {
        id: back
        radius: 40
        color: root.enabled ? (root.selected || root.active ? Qt.lighter(root.color, 1.035) : "transparent") : "#30000000"
        border {
            width: root.active && root.enabled ? 0 : 1
            color: root.color
        }

        Behavior on color { ColorAnimation { duration: 250 } }
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: enabled ? Qt.PointingHandCursor : Qt.ArrowCursor

        onPressed: mouse.accepted = false
        onEntered: {
            parent.selected = true
        }
        onExited: {
            parent.selected = false
        }
    }
}