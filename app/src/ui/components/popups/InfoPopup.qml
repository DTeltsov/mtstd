import QtQuick 2.7


ErrorPopup {
    function setInfo(text, title) {
        if (!title) {
            title = qsTranslate("", "message")
        }
        if (!text) {
            text = qsTranslate("", "unknown")
        }
        console.info(title, " | ", text)
        titlePopupError = title
        textErr = text
        open()
    }
}
