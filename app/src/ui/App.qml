import QtQuick 2.7
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.2

import "qrc:/AColor.js" as Colors
import "qrc:/components/login"
import "qrc:/components/popups"


ApplicationWindow {
    id: app
    minimumHeight: 700
    minimumWidth: 1024

    title: "%1 v%2".arg(Qt.application.name).arg(Qt.application.version)
    color: Colors.dark_3

    FontLoader {
        id: ajaxFont
        source: "qrc:/fonts/robotoRegular.ttf"
    }

    Component {
        id: userAuthorization
        LoginWizard {
            onAuthorized: {
                mainStackView.replace(workspaceComponent)
                userAuthorization.destroy()
            }
        }
    }

    Component {
        id: workspaceComponent
        Workspace {}
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: 0
        StackView {
            id: mainStackView
            Layout.fillWidth: true
            Layout.fillHeight: true
            initialItem: {
                return userAuthorization
            }
            replaceEnter: Transition {
                PropertyAnimation {
                    property: "opacity"
                    from: 0; to: 1
                    duration: 450
                    easing.type: Easing.OutQuad
                }
            }
            replaceExit: Transition {
                PropertyAnimation {
                    property: "opacity"
                    from: 1; to: 0
                    duration: 200
                    easing.type: Easing.InQuad
                }
            }
        }
    }

    ExitDialog {
        id: exitDialog
    }
    onClosing: {
        close.accepted = false
        onTriggered: {
            exitDialog.open()
        }
    }
    ErrorPopup {
        id: errorPopup
    }
    InfoPopup { id: infoPopup }
    LanguagesPopup { id: langPopup }

    PopupQuestionTitle {
        id: criticalErrorPopup
        textBtnOk: qsTranslate("", "ok")
        textBtnCancel: ""

        function setError(text, title) {
            if (!title) { title = qsTranslate("", "error") }
            if (!text) { text = qsTranslate("", "unknown_error") }
            if (!!logger) logger.error("Critical error: " + title + " | " + text)
            criticalErrorPopup.textTitle = title
            criticalErrorPopup.textBody = text
            criticalErrorPopup.open()
        }
        onOk: { Qt.quit() }
    }
}
