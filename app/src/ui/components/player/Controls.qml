import QtQuick 2.7
import QtQuick.Layouts 1.2

import "qrc:/AColor.js" as Colors
import "qrc:/elements"
import "qrc:/theme"
import "qrc:/components"


Rectangle {
    id: root
    color: "transparent"
    property int iconsSize: parent.height * 0.5
    implicitWidth: mainLayout.implicitWidth + 50
    RowLayout {
        id: mainLayout
        anchors.fill: parent
        spacing: 15
        Rectangle {
            Layout.preferredWidth: root.iconsSize
            Layout.preferredHeight: root.iconsSize
            Layout.alignment: Qt.AlignCenter
            color: "transparent"
            Image {
                anchors.fill: parent
                source: "qrc:/elements/previous.svg"
                height: parent.height * 0.8
                width: parent.width * 0.8
            }
            MouseArea {
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                onEntered: {
                    parent.opacity = 0.7
                }
                onExited: {
                    parent.opacity = 1.0
                }
                onClicked: {
                    session.player.previous()
                }
            }
        }
        Rectangle {
            Layout.preferredWidth: root.iconsSize
            Layout.preferredHeight: root.iconsSize
            Layout.alignment: Qt.AlignCenter
            color: "transparent"
            Image {
                anchors.centerIn: parent
                source: {
                    switch (session.player.player_state) {
                        case 1: return "qrc:/elements/pause.svg"
                        default: return "qrc:/elements/play.svg"
                    }
                }
                height: parent.height * 0.8
                width: parent.width * 0.8
            }
            MouseArea {
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                onEntered: {
                    parent.opacity = 0.7
                }
                onExited: {
                    parent.opacity = 1.0
                }
                onClicked: {
                    if (session.player.player_state == 1) {
                        session.player.pause()
                    }
                    else {
                        session.player.play()
                    }
                }
            }
        }
        Rectangle {
            Layout.preferredWidth: root.iconsSize
            Layout.preferredHeight: root.iconsSize
            Layout.alignment: Qt.AlignCenter
            color: "transparent"
            Image {
                anchors.centerIn: parent
                source: "qrc:/elements/next.svg"
                height: parent.height * 0.8
                width: parent.width * 0.8
            }
            MouseArea {
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                onEntered: {
                    parent.opacity = 0.7
                }
                onExited: {
                    parent.opacity = 1.0
                }
                onClicked: {
                    session.player.next()
                }
            }
        }
        Rectangle {
            Layout.preferredWidth: root.iconsSize
            Layout.preferredHeight: root.iconsSize
            Layout.alignment: Qt.AlignCenter
            color: "transparent"
            Image {
                anchors.centerIn: parent
                source: {
                    switch (session.player.repeat_mode) {
                        case 1: return "qrc:/elements/repeating_one.svg"
                        case 2: return "qrc:/elements/repeat.svg"
                        case 3: return "qrc:/elements/repeating.svg"
                        default: return "qrc:/elements/repeat.svg"
                    }
                }
                height: parent.height * 0.8
                width: parent.width * 0.8
            }
            MouseArea {
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                onEntered: {
                    parent.opacity = 0.7
                }
                onExited: {
                    parent.opacity = 1.0
                }
                onClicked: {
                    session.player.changeRepeatMode()
                }
            }
        }
    }
}
