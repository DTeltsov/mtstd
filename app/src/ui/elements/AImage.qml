import QtQuick 2.7
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.2


Image {
    property alias cursorShape: mouseArea.cursorShape
    property alias mouseArea: mouseArea
    property alias hoverEnabled: mouseArea.hoverEnabled

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        cursorShape: enabled ? Qt.PointingHandCursor : Qt.ArrowCursor
    }
}
