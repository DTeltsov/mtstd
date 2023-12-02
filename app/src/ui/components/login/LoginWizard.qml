import QtQuick 2.7

import "qrc:/components/login"


Item {
    id: root
    signal authorized

    Login {
        id: recLogin
        anchors.centerIn: parent
        Connections {
            target: session
            function onSignalStartSession() {
                 root.authorized()
            }
        }
    }
}
