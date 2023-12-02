import QtQuick 2.7
import QtQuick.Layouts 1.2

import "qrc:/AColor.js" as Colors
import "qrc:/elements"
import "qrc:/theme"
import "qrc:/components"


Rectangle {
    color: "black"
    Rectangle {
        id: playerRect
        width: parent.width
        height: 75
        color:  Colors.dark_2
        // Player {
        //     id: player
        // }
    }
    Rectangle {
        id: root
        height: parent.height - playerRect.height
        width: parent.width
        anchors.top: playerRect.bottom

        color:  Colors.dark_3_5
        radius: 12
        Library {
            id: library
        }
    }
}
