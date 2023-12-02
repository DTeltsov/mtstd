import QtQuick 2.7
import QtQuick.Layouts 1.2

import "qrc:/AColor.js" as Colors


Rectangle {
    id: spinner
    objectName: "spinner"
    anchors.centerIn: parent
    color: parent.color
    property int current: 0
    property int rectanglesCount: 5
    onVisibleChanged: {
        visible ? timer.start() : timer.stop()
    }

    Timer {
        id: timer
        interval: 200
        repeat: true
        onTriggered: {
            if (current == rectanglesCount){
                current = 0
                for (var index = 0; index < rectanglesCount; index++){
                    repeaterSpinner.itemAt(index).color = Colors.green_3;
                }
            } else {
                repeaterSpinner.itemAt(current).color = Colors.red_1;
                current += 1
            }
        }
    }

    RowLayout {
        id: layoutSpinner
        anchors.centerIn: parent
        spacing: 10

        Repeater {
            id: repeaterSpinner
            model: rectanglesCount
            Rectangle {
                width: 50;
                height: 50;
                radius: 25
                color: Colors.green_3
            }
        }
    }
}
