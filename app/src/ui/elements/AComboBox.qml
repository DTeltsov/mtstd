import QtQuick 2.7
import QtQuick.Controls 2.3

import "qrc:/AColor.js" as Colors


ComboBox {
    id: control
    property alias textColor: textItem.color
    property string defaultText: ""
    readonly property alias back: backRect
    readonly property alias pop_up: popup
    property int radius: 8

    displayText: currentIndex < 0 ? defaultText : getTextForDisplay(currentText)
    focusPolicy: Qt.NoFocus

    function getTextForDisplay(text) {
        return text
    }
    function getTextColor(text) {
        return Colors.light_2
    }
    contentItem: Text {
        id: textItem
        leftPadding: 10
        width: control.width
        text: control.displayText
        verticalAlignment: Text.AlignVCenter
        font: control.font
        elide: Text.ElideRight
        color: currentIndex === -1 ? Colors.middle_4 : control.getTextColor(text)
    }

    indicator: Image {
        id: ind
        anchors.right: parent.right
        anchors.verticalCenter: parent.verticalCenter
        anchors.rightMargin: width
        visible: enabled
        source: "qrc:/menu/a-chevron-down.svg"
    }

    delegate: ItemDelegate {
        implicitWidth: control.highlightedIndex === index ? Math.max(contentItem.implicitWidth + 25, parent.width) : parent.width

        background: Rectangle {
            implicitWidth: parent.width
            radius: control.radius
            color: Colors.dark_1
            MouseArea {
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor

                onClicked: {
                    control.currentIndex = index
                    popup.close()
                }
                onPressed: {
                    control.currentIndex = index
                    popup.close()
                }

                onEntered: {
                    parent.color = Colors.middle_3
                }
                onExited: {
                    parent.color = Colors.dark_1
                }
            }
        }

        contentItem: Text {
            text: control.getTextForDisplay(modelData)
            color: control.getTextColor(text)
            font: control.font
            elide: Text.ElideRight
            verticalAlignment: Text.AlignVCenter
        }
    }

    background: Rectangle {
        id: backRect
        // implicitWidth: control.width
        implicitHeight: control.height
        color: Colors.dark_1
        radius: control.radius
    }

    popup: Popup {
        id: popup
        objectName: "comboBoxPopup"
        y: control.height
        padding: 0
        width: control.width
        implicitHeight: contentItem.implicitHeight
        contentItem: ListView {
            implicitHeight: contentHeight
            model: control.popup.visible ? control.delegateModel : null
            currentIndex: control.highlightedIndex
            ScrollIndicator.vertical: ScrollIndicator {}
        }
        background: Rectangle {
            radius: control.radius
            color: Colors.dark_1
        }
    }
}
