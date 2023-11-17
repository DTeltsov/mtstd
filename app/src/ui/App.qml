import QtQuick 2.7
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.2

import "qrc:/AColor.js" as Colors
import "qrc:/components/login"
import "qrc:/components/popups"

import AQML 1.0
import AEnums 1.0


ApplicationWindow {
    id: app
    minimumHeight: 700
    minimumWidth: 1024

    title: "%1 v%2".arg(Qt.application.name).arg(Qt.application.version)
    color: Colors.dark_3

    FontLoader {
        id: aFont
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
        Header {
            id: appHeader
            Layout.fillWidth: true
        }

        StackView {
            id: mainStackView
            Layout.fillWidth: true
            Layout.fillHeight: true
            initialItem: userAuthorization
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

        function checkCanClosing() {
            if (storage.infoModel.isTesting){
                errorPopup.setError(qsTranslate("warning", "completed_test_required"),
                                    qsTranslate("", "exit_canceled"))
                return false
            }
            return true
        }
    }
    onClosing: {
        close.accepted = false
        onTriggered: {
            if (exitDialog.checkCanClosing()) {
                exitDialog.open()
            }
        }
    }
    PopupBusy { id: popupBusy }
    ErrorPopup {
        id: errorPopup

        Connections {
            target: db
            function onSignalError(title, body) {errorPopup.setError(body, title)}
        }
        Connections {
            target: storage
            function onSignalError(title, body) {errorPopup.setError(body, title)}
        }
        Connections {
            target: storage && storage.tracker
            function onSignalError(title, body) {errorPopup.setError(body, title)}
        }
    }
    InfoPopup { id: infoPopup }
    PausePopup {}
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
