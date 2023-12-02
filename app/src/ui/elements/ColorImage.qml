import QtQuick 2.7
import QtGraphicalEffects 1.0


Item {
    id: root
    width: image.width
    height: image.height

    property alias image: image
    property alias source: image.source
    property alias sourceSize: image.sourceSize

    property alias color: colorOverlay.color

    Image {
        id: image
        visible: false
    }

    ColorOverlay {  // doesn't work on raspberry ¯\_(ツ)_/¯
        id: colorOverlay
        anchors.fill: image
        source: image
        Behavior on color { ColorAnimation { duration: 250 } }
    }
}
