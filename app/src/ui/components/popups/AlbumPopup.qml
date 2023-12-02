import QtQuick 2.7
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.2
import QtGraphicalEffects 1.15

import "qrc:/AColor.js" as Colors
import "qrc:/elements"
import "qrc:/theme"


Popup {
    id: root
    implicitWidth: 1000
    implicitHeight: 500

    RowLayout {
        id: mainLayout
        spacing: 13
        anchors.fill: parent
        anchors.margins: 10
        Image {
            id: img
            source: session.library.displayAlbum.cover
            Layout.preferredWidth: parent.height * 0.8
            Layout.preferredHeight: parent.height * 0.8
            Layout.alignment: Qt.AlignCenter
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
        }
        ColumnLayout {
            Layout.fillWidth: true
            Layout.topMargin: 48
            Layout.preferredHeight: parent.height * 0.8
            Layout.alignment: Qt.AlignCenter
            Text {
                id: albumTitle
                text: session.library.displayAlbum.title
                horizontalAlignment: Text.AlignHLeft
                font.pixelSize: 20
            }
            Text {
                text: session.library.displayAlbum.artist
                horizontalAlignment: Text.AlignHLeft
                color: Colors.light_1
                font.pixelSize: albumTitle.font.pixelSize * 0.8
            }
            ListView {
                id: view
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.topMargin: 20
                model: session.library.displayAlbum.songs
                clip: true
                spacing: 5
                onOriginYChanged: {
                    contentY += originY
                }

                ScrollBar.vertical: ScrollBar {
                    minimumSize: 0.1

                    contentItem: Rectangle {
                        radius: width * 0.7
                        color: parent.pressed ? Qt.darker(Colors.light_4, 2.2) : Colors.light_4
                        opacity: parent.active || parent.size < 1 ? 0.85 : 0
                        Behavior on opacity { NumberAnimation { duration: 500; easing.type: Easing.OutQuart} }
                    }
                }
                delegate: Rectangle {
                    id: song
                    implicitHeight: 40
                    implicitWidth: 580
                    color: "transparent"
                    ColumnLayout{
                        anchors.fill: parent
                        spacing: 0
                        Rectangle {
                            implicitHeight: 1
                            Layout.fillWidth: true
                            color: "white"
                        }
                        RowLayout {
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            RowLayout {
                                id: songLayout
                                Layout.fillWidth: true
                                Layout.fillHeight: true
                                Image {
                                    id: playThisSong
                                    visible: session.player.song.title == modelData.title
                                    source: "qrc:/elements/playing.svg"
                                    Layout.preferredWidth: song.height * 0.6
                                    Layout.preferredHeight: song.height * 0.6
                                    RotationAnimation {
                                        id: rotate
                                        target: playThisSong
                                        loops: Animation.Infinite
                                        running: playThisSong.visible
                                        property: "rotation"
                                        from: 0
                                        to: 360
                                        duration: 850
                                        direction: RotationAnimation.Clockwise
                                    }
                                }
                                ColumnLayout {
                                    Text {
                                        id: songTitle
                                        Layout.topMargin: 2
                                        Layout.alignment: Qt.AlignLeft
                                        text: modelData.title
                                        lineHeight: 7
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
                                                session.play(modelData.title)
                                            }
                                        }
                                    }
                                    Text {
                                        id: songArtist
                                        Layout.alignment: Qt.AlignLeft
                                        Layout.topMargin: 4
                                        text: modelData.artist
                                        color: Colors.middle_2
                                        font.pixelSize: 10
                                        lineHeight: 1
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
                                                session.play(modelData.title)
                                            }
                                        }
                                    }
                                }
                                MouseArea {
                                    Layout.fillWidth: true
                                    Layout.fillHeight: true
                                    hoverEnabled: true
                                    cursorShape: Qt.PointingHandCursor
                                    onEntered: {
                                        parent.opacity = 0.7
                                    }
                                    onExited: {
                                        parent.opacity = 1.0
                                    }
                                    onClicked: {
                                        session.play(modelData.title)
                                    }
                                }
                            }
                            Rectangle {
                                Layout.fillWidth: true
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
                                        session.play(modelData.title)
                                    }
                                }
                            }
                            Image {
                                id: options
                                source: "qrc:/elements/options.svg"
                                property int size: 5
                                Layout.preferredHeight: options.size
                                Layout.preferredWidth: options.size * 3.12
                                MouseArea {
                                    anchors.fill: parent
                                    cursorShape: Qt.PointingHandCursor
                                    onClicked: {
                                        var RelativeToScreen = options.mapToItem(null, 0, options.height);
                                        optionsPopup.setData(RelativeToScreen.y, RelativeToScreen.x, modelData.title)
                                        optionsPopup.open()
                                    }
                                }
                            }

                        }
                    }
                }
            }
        }
    }
}
