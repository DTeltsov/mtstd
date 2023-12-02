import QtQuick 2.7
import "qrc:/AColor.js" as Colors


Item {
    id: root
    implicitWidth: simpleText.implicitWidth
    implicitHeight: simpleText.implicitHeight

    property alias textComp: simpleText
    property alias text: simpleText.text
    property alias color: simpleText.color
    property alias font: simpleText.font
    property alias horizontalAlignment: simpleText.horizontalAlignment
    property alias verticalAlignment: simpleText.horizontalAlignment
    property alias wrapMode: simpleText.wrapMode
    property alias style: simpleText.style
    property alias styleColor: simpleText.styleColor
    property alias enabled: simpleText.enabled
    property alias lineHeight: simpleText.lineHeight
    property alias lineHeightMode: simpleText.lineHeightMode
    property alias elide: simpleText.elide

    property alias cursorShape: mouseArea.cursorShape
    property alias mouseArea: mouseArea
    property alias hoverEnabled: mouseArea.hoverEnabled
    property alias propagateComposedEvents: mouseArea.propagateComposedEvents

    Text {
        id: simpleText
        color: enabled ? Colors.light_3 : Colors.middle_4
        anchors.fill: parent
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        font.family: ajaxFont.name
        font.pixelSize: 14
        lineHeightMode: Text.FixedHeight
        lineHeight: 20
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent
    }
}