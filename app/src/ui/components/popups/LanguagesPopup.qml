import QtQuick 2.7
import QtQuick.Layouts 1.2

import "qrc:/AColor.js" as Colors
import "qrc:/theme"


Popup {
    id: root
    width: contentItem.implicitWidth + leftPadding + rightPadding
    height: contentItem.implicitHeight + topPadding + bottomPadding
    topPadding: backgroundHeader.height
    bottomPadding: topPadding / 2
    leftPadding: bottomPadding
    rightPadding: leftPadding

    closePolicy: Popup.CloseOnPressOutside | Popup.CloseOnEscape

    enter: Transition {
        NumberAnimation { property: "opacity"; to: 1.0; duration: 50; easing.type: Easing.InExpo }
    }
    exit: Transition {
        NumberAnimation { property: "opacity"; to: 0.0; duration: 200 }
    }

    background: Rectangle {
        anchors.fill: parent
        color: Colors.dark_3
        radius: 20

        Item {
            id: backgroundHeader
            width: parent.width
            height: 60
            clip: true

            Rectangle {
                anchors.fill: parent
                anchors.bottomMargin: -radius
                radius: parent.parent.radius
                color: Colors.dark_4
            }
            Text {
                anchors.fill: parent
                text: qsTranslate("localization", "welcome")
                font.pixelSize: 28
            }
        }
    }

    contentItem: Item {
        implicitWidth: contentLayout.implicitWidth
        implicitHeight: contentLayout.implicitHeight

        ColumnLayout {
            id: contentLayout
            anchors.fill: parent
            spacing: 25

            Text {
                Layout.alignment: Qt.AlignHCenter
                Layout.topMargin: 10
                text: qsTranslate("localization", "choose_language")
                color: Colors.green_2
                font.pixelSize: 16
            }

            GridLayout {
                id: grid
                Layout.fillWidth: true
                Layout.fillHeight: true
                rows: 1
                flow: GridLayout.TopToBottom
                rowSpacing: 30
                columnSpacing: 30

                Repeater {
                    id: repeater
                    model: translator && translator.langs

                    delegate: ColumnLayout {
                        Rectangle {
                            implicitWidth: 120 + imgFlag.anchors.margins * 2
                            implicitHeight: 78 + imgFlag.anchors.margins * 2
                            radius: 12
                            color: translator && translator.lang === model.code ? Colors.green_2 : "transparent"

                            Image {
                                id: imgFlag
                                anchors.fill: parent
                                anchors.margins: 8
                                source: "qrc:/flags/%1.svg".arg(model.code)
                                sourceSize: Qt.size(width, height)
                                MouseArea {
                                    anchors.fill: parent
                                    cursorShape: enabled ? Qt.PointingHandCursor : Qt.ArrowCursor
                                    onClicked: {
                                        translator.installTr(model.code)
                                    }
                                }
                            }
                        }
                        Text {
                            Layout.alignment: Qt.AlignHCenter
                            text: model.label
                            font.pixelSize: 18
                        }
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                    }
                }
            }
            Button {
                Layout.preferredWidth: Math.max(120, contentItem.implicitWidth + 30)
                Layout.alignment: Qt.AlignHCenter
                text: qsTranslate("", "choose")
                font.pixelSize: 16

                onClicked: { root.close() }
            }
        }
    }
}
