import QtQuick 2.7
import QtQuick.Layouts 1.2
import QtGraphicalEffects 1.15
import QtQuick.Controls 2.15

import "qrc:/AColor.js" as Colors
import "qrc:/elements"
import "qrc:/theme"
import "qrc:/components"


Rectangle {
    id: root
    implicitWidth: mainLayout.implicitWidth + 50
    implicitHeight: parent * 0.8
    color: Colors.middle_5
    radius: 10
    RowLayout {
        id: mainLayout
        anchors.fill: parent
        Image {
            id: img
            source: session.player && session.player.song && session.player.song.cover ? session.player.song.cover : ""
            Layout.preferredWidth: root.height
            Layout.preferredHeight: root.height
            layer.enabled: true
            layer.effect: OpacityMask {
                maskSource: Item {
                    width: img.width
                    height: img.height
                    Rectangle {
                        anchors.centerIn: parent
                        width: img.adapt ? img.width : Math.min(img.width, img.height)
                        height: img.adapt ? img.height : width
                        radius: 5
                    }
                }
            }
            MouseArea {
                anchors.fill: parent
                cursorShape: Qt.PointingHandCursor
                onClicked: {
                    if (session.player.song.cover) {
                        albumPopup.open()
                    }
                }
            }
        }
        ColumnLayout {
            visible: session.player.song.title != 'this_song_is_empty'
            Layout.fillWidth: true
            Layout.rightMargin: 10
            ColumnLayout {
                Text {
                    id: songTitle
                    Layout.topMargin: 2
                    Layout.alignment: Qt.AlignCenter
                    text: visible ? session.player.song.title : ""
                    lineHeight: 7
                }
                Text {
                    id: songArtist
                    Layout.alignment: Qt.AlignCenter
                    Layout.topMargin: 4
                    text: visible ? session.player.song.artist : ""
                    color: Colors.middle_2
                    font.pixelSize: 10
                    lineHeight: 1
                }
                RowLayout {
                    Layout.topMargin: 0
                    Text {
                        id: currentTime
                        text: session.player.current_time
                        color: Colors.light_1
                        font.pixelSize: 9
                        lineHeight: 1
                    }
                    Rectangle {
                        Layout.fillWidth: true
                    }
                    Text {
                        id: remainingTime
                        text: session.player.remaining_time
                        color: Colors.light_1
                        font.pixelSize: 9
                        lineHeight: 1
                    }
                }
            }
            Slider {
                id: progressBar
                Layout.preferredWidth: 440
                Layout.preferredHeight: 5
                from: session.player.start
                value: session.player.position
                to: session.player.end
                handle.implicitHeight: 5
                handle.implicitWidth: 5
                onMoved: {
                    session.player.move(value)
                }
            }
        }
    }
}
