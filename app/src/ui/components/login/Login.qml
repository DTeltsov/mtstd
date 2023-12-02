import QtQuick 2.7
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.2

import "qrc:/AColor.js" as Colors
import "qrc:/components/popups"
import "qrc:/elements"
import "qrc:/theme"


Rectangle {
    id: root
    implicitWidth: loginWidget.implicitWidth
    implicitHeight: loginWidget.implicitHeight
    color: Colors.dark_2
    property alias errorItem: errorTitle
    signal authorized

    radius: 13

    function login(login, password) {
        session.login(login, password, '')
    }

    ColumnLayout {
        id: loginWidget
        spacing: 0
        anchors.fill: parent
        Rectangle {
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignTop
            height: 73
            color: Colors.dark_4
            radius: root.radius
            Text {
                id: head
                anchors.fill: parent
                font.pixelSize: 18
                text: qsTranslate("localization", "welcome")
                color: Colors.light_2
            }
            Rectangle {
                width: parent.width
                height: parent.radius
                color: parent.color
                anchors {
                    bottom: parent.bottom
                    left: parent.left
                    right: parent.right
                }
            }

        }

        ColumnLayout {
            Layout.fillHeight: true
            Layout.fillWidth: true
            Layout.leftMargin: 50
            Layout.rightMargin: 50
            Layout.bottomMargin: 14
            spacing: 10

            AInputField {
                id: loginName
                objectName: "loginField"
                text: ""
                height: 40

                placeholderText: qsTranslate("authorization", "login")
                marginLeft: 14
                radius: 8
                border {
                    width: 0
                    color: "#009c63"
                }
                onFocusTextInputChanged: {
                    if (loginName.focusTextInput){
                        loginName.border.width = 2
                    } else {
                        loginName.border.width = 0
                    }
                }
                Keys.onReturnPressed: {
                    btnLogin.forceActiveFocus()
                    login(loginName.text, password.text)
                }
            }

            AInputField {
                id: password
                objectName: "passwordField"
                text: ""
                placeholderText: qsTranslate("authorization", "password")
                echoMode: TextInput.Password
                marginLeft: 14
                radius: 8
                border {
                    width: 0
                    color: "#009c63"
                }
                onFocusTextInputChanged: {
                    if (password.focusTextInput){
                        password.border.width = 2
                    } else {
                        password.border.width = 0
                    }
                }
                Keys.onReturnPressed: {
                    btnLogin.forceActiveFocus()
                    login(loginName.text, password.text)
                }
            }

            Text {
                id: errorTitle
                objectName: "loginErrorText"
                implicitWidth: 300
                Layout.topMargin: 6
                Layout.bottomMargin: 6
                Layout.preferredHeight: height
                text: ""
                color: Colors.red_1
                visible: !!text
                wrapMode: Text.WordWrap
            }

            RowLayout {
                spacing: 10

                Button {
                    id: btnLogin
                    objectName: "loginBtn"
                    text: qsTranslate("authorization", "log_in")
                    height: 40
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignVCenter
                    onClicked: login(loginName.text, password.text)
                    Keys.onReturnPressed: {
                        login(loginName.text, password.text)
                    }
                }
            }
        }
    }
    Spinner {
        id: loadSpinner
        visible: false
    }
}
