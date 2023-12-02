import QtQuick 2.7
import QtQuick.Controls 2.3

import "qrc:/components/popups"


PopupQuestionTitle {
    id: dialog
    opacity: 0
    textTitle: ""
    textBody: qsTranslate("", "close_question")
    textBtnOk: qsTranslate("", "no")
    textBtnCancel: qsTranslate("", "yes")
    closePolicy: Popup.CloseOnPressOutside | Popup.CloseOnEscape

    onCancel: {
        logger.info('APP HAS BEEN CLOSED BY USER')
        Qt.quit()
    }
    function checkCanClosing() {
        return true
    }

    enter: Transition {
        NumberAnimation { property: "opacity"; to: 1.0; duration: 30; easing.type: Easing.InExpo }
    }
    exit: Transition {
        NumberAnimation { property: "opacity"; to: 0.0; duration: 200 }
    }
}
