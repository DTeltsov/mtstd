import QtQuick 2.7

import "qrc:/AColor.js" as Colors
import "qrc:/theme"


Popup {
    id: root
    parent: parent
    y: parent.height
    implicitWidth: codeItem.implicitWidth
    implicitHeight: codeItem.implicitHeight
//    closePolicy: Popup.CloseOnPressOutside

    property alias back: canvas
    property alias textEdit: textEdit
    signal processInput(string text)

    onOpened: {
        canvas.requestPaint()
    }
    onClosed: {
        textEdit.text = ''
    }
    background: Canvas {
        id: canvas
//        antialiasing: true
        property int radius: 10
        property int tailPoint: -root.x + root.parent.width / 2
        property int lineWidth: 4
        property int shadowBlur: 3
        property int margin: 16
        property color borderColor: !textEdit.text ? Colors.green_1 : Colors.yellow_1
        onBorderColorChanged: canvas.requestPaint()
        Behavior on borderColor { ColorAnimation { duration: 300 } }
        property color color: Colors.dark_1

        onPaint: {
            var ctx = getContext("2d");
            ctx.reset()
            ctx.shadowBlur = canvas.shadowBlur
            ctx.shadowColor = canvas.borderColor
            ctx.strokeStyle = canvas.borderColor
            ctx.fillStyle = canvas.color
            ctx.lineJoin = 'round'
            ctx.lineWidth = canvas.lineWidth
            let delta = 25
            var leftTop = Qt.point(canvas.lineWidth + canvas.shadowBlur, canvas.margin)
            var rightBottom = Qt.point(width - canvas.lineWidth - canvas.shadowBlur, height - canvas.lineWidth - canvas.shadowBlur)

            ctx.beginPath();
            function arcTo(fromX, fromY, toX, toY, radiusScale, mode) {
                let start = Qt.point(fromX, fromY)
                let end = Qt.point(toX, toY)
                let midle = Qt.point((start.x + end.x) / 2, (start.y + end.y) / 2)
                let distanceMS = Math.pow(Math.pow(midle.x - start.x, 2) + Math.pow(midle.y - start.y, 2), 0.5)

                let distanceMC = distanceMS * Math.pow(radiusScale * radiusScale - 1, 0.5)
                let normal = Qt.point(start.y - end.y, end.x - start.x)
                let normalLenght = Math.pow(normal.x * normal.x + normal.y * normal.y, 0.5)
                normal.x = normal.x / normalLenght
                normal.y = normal.y / normalLenght

                let center
                if (mode == "up") {
                    center = Qt.point(midle.x - normal.x * distanceMC, midle.y - normal.y * distanceMC)
                } else {
                    center = Qt.point(midle.x + normal.x * distanceMC, midle.y + normal.y * distanceMC)
                }
                let alphaStart = Math.atan2(start.y - center.y, start.x - center.x)
                let alphaEnd = Math.atan2(end.y - center.y, end.x - center.x)
                if (mode == "up") alphaEnd -= 2 * Math.PI

                ctx.arc(center.x, center.y, radiusScale * distanceMS, alphaStart, alphaEnd);
//                console.log(start, end, midle, distanceMS, distanceMC, normal, center)
//                console.log(Math.atan2(start.y - center.y, start.x - center.x) * 180 / Math.PI, Math.atan2(end.y - center.y, end.x - center.x) * 180 / Math.PI)
            }
            ctx.arc(leftTop.x + canvas.radius, leftTop.y + canvas.radius, canvas.radius, 180 * Math.PI/180, 270 * Math.PI/180);
            let leftPoint = Qt.point(Math.max(leftTop.x + canvas.radius, canvas.tailPoint - delta), leftTop.y)
            arcTo(leftPoint.x, leftPoint.y, leftPoint.x + delta, canvas.lineWidth, 2, "up")
            arcTo(leftPoint.x + delta, canvas.lineWidth, leftPoint.x + 2 * delta, leftTop.y, 2, "up")
            ctx.lineTo(rightBottom.x - canvas.radius, leftTop.y);
            ctx.arc(rightBottom.x - canvas.radius, leftTop.y + canvas.radius, canvas.radius, -90 * Math.PI/180, 0);
            ctx.lineTo(rightBottom.x, rightBottom.y - canvas.radius);
            ctx.arc(rightBottom.x - canvas.radius, rightBottom.y - canvas.radius, canvas.radius, 0, 90 * Math.PI/180);
            ctx.lineTo(leftTop.x + canvas.radius, rightBottom.y);
            ctx.arc(leftTop.x + canvas.radius, rightBottom.y - canvas.radius, canvas.radius, 90 * Math.PI/180, 180 * Math.PI/180);

            ctx.closePath();
            ctx.stroke();
            ctx.fill();
        }
    }
    contentItem: Item {
        id: codeItem
        implicitWidth: Math.max(textEdit.implicitWidth + 40, 2 * canvas.radius + 50 + 20)
        implicitHeight: 50

        TextInput {
            id: textEdit
            anchors.fill: parent
            anchors.margins: canvas.lineWidth + canvas.shadowBlur
            anchors.topMargin: canvas.margin
            anchors.leftMargin: anchors.margins + 10

            echoMode: TextInput.Normal
            text: ""
            color: Colors.light_1

            activeFocusOnTab: true
            focus: true

            verticalAlignment: TextEdit.AlignVCenter

            cursorVisible: false
            selectByMouse: true
            selectionColor: canvas.borderColor

            Keys.onReturnPressed: {
                root.processInput(textEdit.text)
                textEdit.text = ''
            }
        }
    }
    enter: Transition {
        NumberAnimation { property: "opacity"; to: 1.0; duration: 50; easing.type: Easing.InExpo }
    }
    exit: Transition {
        NumberAnimation { property: "opacity"; to: 0.0; duration: 150 }
    }
}
