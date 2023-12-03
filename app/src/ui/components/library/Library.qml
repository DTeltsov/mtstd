import QtQuick 2.7
import QtQuick.Controls 2.3
import QtGraphicalEffects 1.15
import QtQuick.Layouts 1.2

import "qrc:/AColor.js" as Colors
import "qrc:/elements"
import "qrc:/theme"

import AQML 1.0


Rectangle {
    id: root
    anchors.fill: parent
    color: Colors.dark_2
    ListView {
        id: songsView
        visible: session.library.mode == "songs"
        model: session.library.songs
        anchors.fill: parent
        anchors.margins: 20
        clip: true
        delegate: Rectangle {
            id: song
            implicitHeight: 40
            implicitWidth: 1487
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
                        Image {
                            id: img
                            source: modelData.cover
                            Layout.preferredWidth: song.height * 0.6
                            Layout.preferredHeight: song.height * 0.6
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
    GridLayout {
        id: albumView
        visible: session.library.mode == "albums"
        anchors.fill: parent
        columns: 6
        Repeater {
            model: session.library.albums
            delegate: Rectangle {
                Layout.preferredWidth: 250
                Layout.preferredHeight: 250
                Layout.alignment: Qt.AlignTop
                Layout.margins: 10
                color: "transparent"

                ColumnLayout {
                    anchors.fill: parent
                    Image {
                        id: img
                        source: modelData.cover
                        Layout.preferredWidth: parent.width * 0.8
                        Layout.preferredHeight: parent.height * 0.8
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

                    Text {
                        text: modelData.title
                        horizontalAlignment: Text.AlignHLeft
                    }

                    Text {
                        text: modelData.artist
                        horizontalAlignment: Text.AlignHLeft
                        color: Colors.light_1
                        font.pixelSize: 10
                    }
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
                        session.showAlbum(modelData.title)
                        albumPopup.open()
                    }
                }
            }
        }
    }
}