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

