import QtQuick 2.0
import io.thp.pyotherside 1.0

Image {
    id: image
    width: 300
    height: 300

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
