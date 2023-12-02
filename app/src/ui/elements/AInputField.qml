import QtQuick 2.7

import "qrc:/AColor.js" as Colors


Rectangle {
    id: recTextInput
    property alias textEdit: textEdit
    property alias text: textEdit.text
    property alias echoMode: textEdit.echoMode
    property alias validator: textEdit.validator
    property alias focusTextInput: textEdit.focus
    property alias wrapMode: textEdit.wrapMode
    property alias textColor: text.color
    property alias cursorHorizontalAlignment: textEdit.horizontalAlignment
    property alias cursorVerticalAlignment: textEdit.verticalAlignment
    property alias placeholderHorizontalAlignment: text.horizontalAlignment
    property alias placeholderVerticalAlignment: text.verticalAlignment
    property var marginLeft: 10
    property string placeholderText: "PlaceHolder"
    color: Colors.dark_1
    clip: true

    width: 300
    height: 40
    radius: height * 0.5
    border.width: 1.5
    border.color: Colors.green_1

    TextInput {
        id: textEdit

        echoMode: TextInput.Normal
        anchors.fill: parent
        anchors.leftMargin: marginLeft
        text: "TextEdit"
        color: Colors.white

        activeFocusOnTab: true

        horizontalAlignment: TextEdit.AlignHCenter
        verticalAlignment: TextEdit.AlignVCenter

        cursorVisible: false
        selectByMouse: true
        selectionColor: Colors.light_4

        Text {
            id: text
            text: placeholderText
            color: Colors.middle_3
            visible: !textEdit.text && !textEdit.activeFocus
            anchors.fill: parent
            horizontalAlignment: placeholderHorizontalAlignment
            verticalAlignment: TextEdit.AlignVCenter
        }
    }
}
