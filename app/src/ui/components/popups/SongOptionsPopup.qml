import QtQuick 2.7
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.2

import "qrc:/AColor.js" as Colors
import "qrc:/elements"
import "qrc:/theme"


Popup {
    id: root
    width: layout.implicitWidth
    height: layout.implicitHeight
    property string songTitle: ""
    property int parentY: 0
    function setData(y, x, title) {
        root.songTitle = title
        root.y = y + 5
        root.x = x - 40
    }

    contentItem: ColumnLayout {
        id: layout
        spacing: 0
        anchors.centerIn: parent
        property int childWidth: 100
        property int childHeight: 30
        Rectangle {
            Layout.preferredWidth: layout.childWidth
            Layout.preferredHeight: layout.childHeight
            color: "transparent"
            Text {
                anchors.fill: parent
                text: qsTranslate("login_errors", "play_next")
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
                    session.playNext(root.songTitle)
                    root.close()
                }
            }
        }
        Rectangle {
            implicitHeight: 1
            Layout.fillWidth: true
            color: "white"
        }
        Rectangle {
            Layout.preferredWidth: layout.childWidth
            Layout.preferredHeight: layout.childHeight
            color: "transparent"
            Text {
                anchors.fill: parent
                text: qsTranslate("login_errors", "play_later")
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
                    session.playLater(root.songTitle)
                    root.close()
                }
            }
        }
        Rectangle {
            implicitHeight: 1
            Layout.fillWidth: true
            color: "white"
        }
        Rectangle {
            Layout.preferredWidth: layout.childWidth
            Layout.preferredHeight: layout.childHeight
            color: "transparent"
            Text {
                anchors.fill: parent
                text: qsTranslate("login_errors", "delete")
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
                    session.delete(root.songTitle)
                    root.close()
                }
            }
        }
    }
}
