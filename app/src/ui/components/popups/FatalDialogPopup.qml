import QtQuick 2.7
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.2

import "qrc:/AColor.js" as Colors
import "qrc:/elements"
import "qrc:/theme"


Popup {
    id: fatalPopup
    objectName: "fatalPopup"
    width: 400
    padding: 20
    closePolicy: Popup.NoAutoClose

    property alias textTitle: title.text
    property alias textBody: body.text


    property alias loader: loader

    property var busyVisible: false


    signal ok

    onClosed: {
        Qt.quit()
    }

    function showError(title, error){
        if (!title) {title = qsTranslate("", "error")}
        if (!error) {error = qsTranslate("", "unknown_error")}
        fatalPopup.busyVisible = true
        fatalPopup.textTitle = title
        fatalPopup.textBody = error
        fatalPopup.open()
    }

    contentItem: ColumnLayout {
        onImplicitHeightChanged: {
            // resolving problem with assigment implicitHeight (Qt 5.14.2)
            fatalPopup.implicitHeight = Math.max(260, implicitHeight)
        }
        spacing: 20
        // title
        Text {
            id: title
            height: 24
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignCenter
            text: "title"
            color: Colors.light_1
            font.pixelSize: 18
        }
        // Body
        Text {
            id: body
            Layout.fillHeight: true
            Layout.fillWidth: true
            Layout.topMargin: 30
            Layout.bottomMargin: 15
            text: "Body text"
            color: Colors.light_1
            wrapMode: Text.WordWrap
            font.pixelSize: 16
        }
        Loader {
            id: loader
            Layout.fillWidth: true
        }
        // separator
        Rectangle {
            color: Colors.red_2
            opacity: 0.3
            width: 350
            height: 1
            Layout.alignment: Qt.AlignCenter
            Layout.fillWidth: true
        }
        RowLayout {
            Layout.fillWidth: true
            spacing: 25
            Layout.alignment: Qt.AlignCenter

            Loader {
                Layout.alignment: Qt.AlignCenter
                sourceComponent: fatalPopup.busyVisible ? busyInd : btnOk
            }

            Component {
                id: btnOk
                ColorButton {
                    width: 150
                    text: qsTranslate("", "ok")
                    color: Colors.red_2
                    item.font.pixelSize: 16
                    onClicked: { ok(); fatalPopup.close() }
                }
            }

            Component {
                id: busyInd
                BusyIndicator {
                    width: 50
                    palette.dark: Colors.red_2
                    running: true
                }
            }
        }

    }
}
