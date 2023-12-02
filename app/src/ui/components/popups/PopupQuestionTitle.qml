import QtQuick 2.7
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.2

import "qrc:/AColor.js" as Colors
import "qrc:/elements"
import "qrc:/theme"


Popup {
    id: questionPopup
    objectName: "questionPopup"
    width: 400
    padding: 20
    closePolicy: Popup.NoAutoClose

    property alias textTitle: title.text
    property alias textBody: body.text

    property alias textBtnOk: btnOk.text
    property alias textBtnCancel: btnCancel.text
    property alias loader: loader

    signal ok
    signal cancel

    contentItem: ColumnLayout {
        onImplicitHeightChanged: {
            // resolving problem with assigment implicitHeight (Qt 5.14.2)
            questionPopup.implicitHeight = Math.max(260, implicitHeight)
        }
        spacing: 20
        // title
        Text {
            id: title
            height: 24
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignCenter
            text: "title"
            color: Colors.light_2
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
            wrapMode: Text.WordWrap
            font.pixelSize: 16
        }
        Loader {
            id: loader
            Layout.fillWidth: true
        }
        // separator
        Rectangle {
            color: Colors.middle_3
            opacity: 0.3
            width: 350
            height: 1
            Layout.alignment: Qt.AlignCenter
            Layout.fillWidth: true
        }
        // buttons
        RowLayout {
            Layout.fillWidth: true
            spacing: 25
            // ok button
            ColorButton {
                id: btnOk
                objectName: "declineQuestionBtn"
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignCenter
                visible: !!text
                color: Colors.light_2
                item.font.pixelSize: 16

                onClicked: { ok(); questionPopup.close() }
            }
            // cancel button
            ColorButton {
                id: btnCancel
                objectName: "confirmQuestionBtn"
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignCenter
                visible: !!text
                color: Colors.red_2
                item.font.pixelSize: 16

                onClicked: { cancel(); questionPopup.close() }
            }
        }
    }
}
