import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3
import QtQuick.Controls.Material 2.1

import "qrc:/AColor.js" as Colors
import "qrc:/AKeyboard.js" as Board

Item {
    id: main
    signal keypress(string key)
    signal backspace()
    signal enter()
    signal switch_language(string value)
    width: 440
    height: 210
    property bool alt_mode: false
    property string language: 'en'

    FontLoader { id: roboto; source: "qrc:/fonts/robotoRegular.ttf" }

    ColumnLayout {
        anchors.fill: parent

        RowLayout {
            spacing: 3
            Layout.alignment: Qt.AlignCenter

            Repeater {
                model: Board.languages[language].rows[0]
                objectName: "repeater1"
                AKeyboardButton {
                    text: modelData
                    text_alt: Board.languages[language].rows_alt[0][index]
                    alt_mode: main.alt_mode
                    objectName: "keyboard" + index
                    onKeypress: main.keypress(key)
                }
            }

            AKeyboardButton {
                width: 34
                objectName: "backspace"
                alt_mode: main.alt_mode
                onKeypress: main.backspace()
                Image {
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.verticalCenter: parent.verticalCenter
                    source: "qrc:/icons/delete-button.png"
                }
            }
        }

        RowLayout {
            spacing: 3
            Layout.alignment: Qt.AlignCenter

            Repeater {
                model: Board.languages[language].rows[1]
                objectName: "repeater2"
                AKeyboardButton {
                    text: modelData
                    text_alt: Board.languages[language].rows_alt[1][index]
                    alt_mode: main.alt_mode
                    onKeypress: main.keypress(key)
                }
            }
        }

        RowLayout {
            spacing: 3
            Layout.alignment: Qt.AlignCenter

            AKeyboardButton {
                width: 34
                objectName: "alt_mode"
                alt_mode: main.alt_mode
                onKeypress: main.alt_mode = !main.alt_mode
                Image {
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.verticalCenter: parent.verticalCenter
                    source: "qrc:/icons/shift.png"
                }
            }

            Repeater {
                model: Board.languages[language].rows[2]
                objectName: "repeater3"
                AKeyboardButton {
                    text: modelData
                    text_alt: Board.languages[language].rows_alt[2][index]
                    alt_mode: main.alt_mode
                    onKeypress: main.keypress(key)
                }
            }

            AKeyboardButton {
                width: 50
                objectName: "Enter"
                alt_mode: main.alt_mode
                color: Colors.middle_4
                onKeypress: main.enter()
                Image {
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.verticalCenter: parent.verticalCenter
                    height: 25
                    width: 30
                    sourceSize.width: 50
                    sourceSize.height: 50
                    source: "qrc:/icons/enter.png"
                }
            }
        }

        RowLayout {
            spacing: 3
            Layout.alignment: Qt.AlignCenter

            Repeater {
                model: Board.languages[language].rows[3]
                objectName: "repeater4"
                AKeyboardButton {
                    text: modelData
                    text_alt: Board.languages[language].rows_alt[3][index]
                    alt_mode: main.alt_mode
                    onKeypress: main.keypress(key)
                }
            }
        }

        RowLayout {
            spacing: 3
            Layout.alignment: Qt.AlignCenter

            AKeyboardButton {
                width: 52
                alt_mode: main.alt_mode
                objectName: "change_lang"
                onKeypress: switch_language(language_label.text)
                Layout.alignment: Qt.AlignCenter
                Text {
                    id: language_label
                    text: "en"
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.verticalCenter: parent.verticalCenter
                    font.pixelSize: 13
                    font.family: roboto.name
                    color: Colors.white
                }
            }

            AKeyboardButton {
                text: " "
                text_alt: " "
                objectName: "space"
                width: 235
                alt_mode: main.alt_mode
                onKeypress: main.keypress(key)
                Text {
                    text: qsTranslate("keyboard","space")
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.verticalCenter: parent.verticalCenter
                    font.pixelSize: 13
                    font.family: roboto.name
                    color: Colors.white
                }
            }
        }
    }

    onSwitch_language: {
        var languages = Object.keys(Board.languages)
        var index = languages.indexOf(value) + 1
        var next_language = languages[index < languages.length ? index : index - languages.length]
        main.language = next_language
        language_label.text = next_language
    }
}
