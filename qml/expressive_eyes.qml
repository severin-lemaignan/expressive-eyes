import QtQuick 2.0
import Sailfish.Silica 1.0
import io.thp.pyotherside 1.0

 ApplicationWindow {
     initialPage: Component {
Page {
    id: expressiveeyes
    allowedOrientations: Orientation.LandscapeMask

    Rectangle {
        color: 'black'
	anchors.fill: parent
	}

Image {
    id: image
    width: 600
    height: 300

    anchors.centerIn: parent

    Python {
        Component.onCompleted: {
            // Add the directory of this .qml file to the search path
            addImportPath(Qt.resolvedUrl('.'));

            importModule('render', function () {
                image.source = 'image://python/face.png';
            });
        }

        onError: console.log('Python error: ' + traceback)
    }
}
}
}
}
