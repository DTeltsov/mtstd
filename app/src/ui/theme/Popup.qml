import QtQuick 2.7
import QtQuick.Controls 2.3

import "qrc:/AColor.js" as Colors


Popup {
    id: root
    parent: app.overlay
    x: Math.round((parent.width - width) / 2)
    y: Math.round((parent.height - height) / 2)
    implicitWidth: 400
    implicitHeight: 300

    focus: true
    modal: true
    closePolicy: Popup.CloseOnPressOutside

    margins: 0
    padding: 0

    readonly property alias back: back

    background: Rectangle {
        id: back
        anchors.fill: parent
        color: Colors.dark_2

        radius: 25
    }

    Overlay.modal: Rectangle {
        color: "#80000000"  // darkening of the background
    }
}