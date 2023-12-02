import QtQuick 2.7


Rectangle {
    height: isVertical ? parent.height : parent.radius
    width: isVertical ? parent.radius : parent.width
    z: parent.z - 1

    color: parent.color

    property bool isVertical: false
}
