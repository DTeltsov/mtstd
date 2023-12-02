import QtQuick 2.7
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.2

import "qrc:/AColor.js" as Colors
import "qrc:/elements"
import "qrc:/theme"


Popup {
    id: root
    objectName: "errorPopup"
    implicitWidth: 420
    implicitHeight: 320
    signal confirmed

    property string titlePopupError: qsTranslate("", "error")
    property string textErr: ""
    property string buttonText: qsTranslate("", "clearly")

    function setError(text, title) {
        if (!title) {
            title = qsTranslate("", "error")
        }
        if (!text) {
            text = qsTranslate("", "unknown_error")
        }
        console.error(title, " | ", text)
        root.titlePopupError = title
        root.textErr = text
        root.open()
    }

    ColumnLayout {
        spacing: 13
        anchors.fill: parent

        Text {
            Layout.alignment: Qt.AlignHCenter
            Layout.preferredWidth: width
            Layout.preferredHeight: 24
            Layout.topMargin: 35

            text: root.titlePopupError
            font.pixelSize: 20
            font.bold: true
            color: Colors.light_2
        }
        Item {
            id: item
            clip: true
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.margins: 15
            Flickable {
                id: scrollArea
                anchors.fill: parent
                contentHeight: Math.max(textError.height, item.height)
                ScrollBar.vertical: ScrollBar {
                    policy: scrollArea.contentHeight > scrollArea.height ? ScrollBar.AlwaysOn : ScrollBar.AlwaysOff
                }
                Text {
                    id: textError
                    objectName: "errorText"
                    text: root.textErr
                    font.pixelSize: 16
                    color: Colors.middle_1
                    wrapMode: Text.WordWrap
                    width: parent.width
                    anchors.centerIn: parent
                }
            }
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 1
            opacity: 0.3
            color: Colors.middle_3
        }

        ColorButton {
            objectName: "errorBtn"
            Layout.preferredWidth: 250
            Layout.bottomMargin: 20
            color: Colors.light_2
            text: root.buttonText
            Layout.alignment: Qt.AlignCenter

            onClicked: {
                root.confirmed()
                root.close()
            }
        }
    }
}