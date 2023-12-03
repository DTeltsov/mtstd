import QtQuick 2.7
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.2

import "qrc:/AColor.js" as Colors
import "qrc:/elements"
import "qrc:/theme"
import "qrc:/components"
import "qrc:/components/header"
import "qrc:/components/library"
import "qrc:/components/popups"

Rectangle {
    color: "black"
    ColumnLayout {
        anchors.fill: parent
        spacing: 0
        Header {
            id: header
            Layout.fillWidth: true
        }
        RowLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 0
            Rectangle {
                Layout.fillHeight: true
                Layout.preferredWidth: 200
                color: Colors.dark_4
                ColumnLayout {
                    anchors.fill: parent
                    ColumnLayout {
                        spacing: 0
                        Rectangle {
                            Layout.fillWidth: true
                            Layout.preferredHeight: 30
                            color: Colors.black
                            Text {
                                anchors.fill: parent
                                text: qsTranslate("login_errors", "your_library")
                            }
                        }
                        Rectangle {
                            Layout.fillWidth: true
                            Layout.preferredHeight: 30
                            color: Colors.dark_3
                            Text {
                                anchors.fill: parent
                                text: qsTranslate("login_errors", "albums")
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
                                    session.library.mode = "albums"
                                }
                            }
                        }
                        Rectangle {
                            Layout.fillWidth: true
                            Layout.preferredHeight: 30
                            color: Colors.dark_3
                            Text {
                                anchors.fill: parent
                                text: qsTranslate("login_errors", "songs")
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
                                    session.library.mode = "songs"
                                }
                            }
                        }
                    }
                }
            }
            StackView {
                id: stackView
                Layout.fillWidth: true
                Layout.fillHeight: true
                initialItem: {
                    return library
                }
                replaceEnter: Transition {
                    PropertyAnimation {
                        property: "opacity"
                        from: 0;
                        to: 1
                        duration: 450
                        easing.type: Easing.OutQuad
                    }
                }
                replaceExit: Transition {
                    PropertyAnimation {
                        property: "opacity"
                        from: 1;
                        to: 0
                        duration: 200
                        easing.type: Easing.InQuad
                    }
                }
            }
        }
    }
    Component {
        id: library
        LibraryWizard {}
    }
    SongOptionsPopup {
        id: optionsPopup
    }
    AlbumPopup { id: albumPopup }
}

