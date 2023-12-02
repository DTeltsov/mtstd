import QtQuick 2.7
import QtQuick.Layouts 1.2

import "qrc:/AColor.js" as Colors
import "qrc:/elements"
import "qrc:/theme"
import "qrc:/components/player"


Rectangle {
    id: root
    height: parent.height
    color: "transparent"
    RowLayout {
        anchors.fill: parent
        Rectangle {
            Layout.fillWidth: true
        }
        Controls {
            id: controls
            Layout.alignment: Qt.AlignCenter
            Layout.preferredHeight: root.height
        }
        Rectangle {
            Layout.fillWidth: true
        }
        SongPlaying {
            id: songPlaying
            Layout.alignment: Qt.AlignCenter
            Layout.preferredHeight: root.height
            Layout.preferredWidth: 500
        }
        Rectangle {
            Layout.fillWidth: true
        }
    }
}
