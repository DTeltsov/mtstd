
import QtQuick 2.7
import QtQuick.Layouts 1.2

import "qrc:/AColor.js" as Colors
import "qrc:/elements"
import "qrc:/theme"
import "qrc:/components/player"


Rectangle {
    implicitHeight: 50
    color: Colors.dark_3
    RowLayout {
        anchors.fill: parent
        Player {
            id: player
            Layout.preferredHeight: parent.height
            Layout.preferredWidth: 1350
        }
    }
}