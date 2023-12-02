import QtQuick 2.7
import QtQuick.Controls 2.3
import QtGraphicalEffects 1.15
import QtQuick.Layouts 1.2

import "qrc:/AColor.js" as Colors
import "qrc:/elements"
import "qrc:/theme"

import AQML 1.0


Rectangle {
    implicitWidth: root.implicitWidth
    implicitHeight: root.implicitHeight

    color: Colors.dark_2
    GridLayout {
        id: root
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