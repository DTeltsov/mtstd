import QtQuick 2.7
import QtQuick.Controls 2.3

import "qrc:/AColor.js" as Colors
import "qrc:/theme"


Button {
    id: root
    implicitWidth: 60
    implicitHeight: 50
    text: "colorButton"
    activeFocusOnTab: false

    property string bordercolor: Colors.black
    property string bgcolor: Colors.middle_1_5

    contentItem: Text {
        id: item
        anchors.centerIn: parent
        width: root.width
        text: root.text
        color: Colors.black
        elide: Text.ElideRight
    }

    background: Rectangle {
        id: back
        radius: 5
        color: root.bgcolor
        border {
            color: root.bordercolor
        }
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: enabled ? Qt.PointingHandCursor : Qt.ArrowCursor
        onClicked: storage.tracker.button_pressed(root.text)
    }
}