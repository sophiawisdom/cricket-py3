#!/bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd ${DIR}

if [ "$1" == "release" ]; then
    DEBUG=0
elif [ "$1" == "debug" ]; then
    DEBUG=1
else
    echo "Usage: ./deploy.sh [debug|release]"
    exit 1
fi

echo rm -r ./dist
rm -r ./dist
echo mkdir ./dist
mkdir ./dist

ditto -v --norsrc --noqtn --noacl /usr/local/opt/qt5/ ./dist/qt5/
ditto -v --norsrc --noqtn --noacl /usr/local/opt/pyqt5/ ./dist/pyqt5/

chown -R $(whoami):staff dist/
chmod -R +w dist/

QT5_VER=$(basename $(readlink /usr/local/opt/qt5))
QT5_DIR="/usr/local/Cellar/qt5/${QT5_VER}"

if [ ! -d "$QT5_DIR" ]; then
    echo "QT5 directory '${QT5_DIR}' doesn't exist."
    exit 1
fi

rm -r ./dist/qt5/libexec/
rm -r ./dist/qt5/mkspecs/
rm -r ./dist/qt5/lib/cmake/
rm -r ./dist/qt5/lib/pkgconfig/
rm -r ./dist/qt5/imports/
rm -r ./dist/qt5/qml/

find ./dist/qt5/bin -type f | grep -v \\.pl$ | xargs -n 1 ./distbuilder/repath-binary.sh ${QT5_DIR}/ @executable_path/../
find ./dist/qt5/lib -type f | egrep "lib/([^/]*?).framework/Versions/[^/]*?/\1$" | xargs -n 1 ./distbuilder/repath-binary.sh ${QT5_DIR}/ @loader_path/../../../../
find ./dist/qt5/plugins -type f | egrep "plugins/([^/]*?)/[^/]*?.dylib" | xargs -n 1 ./distbuilder/repath-binary.sh ${QT5_DIR}/ @loader_path/../../
find ./dist/pyqt5/lib/python2.7/site-packages/PyQt5 -type f | grep \\.so$ | xargs -n 1 ./distbuilder/repath-binary.sh /usr/local/opt/qt5/ @loader_path/../../../../../qt5/

./dist/qt5/bin/qtdiag

python ./distbuilder/buildapp.py ./dist/Cricket.app
clang ./distbuilder/stub.m -isysroot $(xcrun --show-sdk-path) -framework Python -framework Foundation -o ./dist/Cricket.app/Contents/MacOS/Cricket
mkdir -p ./dist/Cricket.app/Contents/Resources/pythonfiles/
cp ./distbuilder/main.py ./dist/Cricket.app/Contents/Resources/pythonfiles/
cp ./distbuilder/app.icns ./dist/Cricket.app/Contents/Resources/app.icns

if [ "${DEBUG}" == "1" ]; then
    ln -s ../../../../../ide ./dist/Cricket.app/Contents/Resources/pythonfiles/ide
    ln -s ../../../../../analysis ./dist/Cricket.app/Contents/Resources/pythonfiles/analysis
    ln -s ../../../../../externals ./dist/Cricket.app/Contents/Resources/pythonfiles/externals
else
    ditto ./ide/ ./dist/Cricket.app/Contents/Resources/pythonfiles/ide/
    ditto ./analysis/ ./dist/Cricket.app/Contents/Resources/pythonfiles/analysis/
    ditto ./externals/ ./dist/Cricket.app/Contents/Resources/pythonfiles/externals/
    ditto ./cli/ ./dist/Cricket.app/Contents/Resources/pythonfiles/cli/
    ditto ./demos/ ./dist/Cricket.app/Contents/Resources/pythonfiles/demos/

    mv ./dist/qt5 ./dist/Cricket.app/Contents/Resources/
    mv ./dist/pyqt5 ./dist/Cricket.app/Contents/Resources/
    mkdir ./dist/Cricket.app/Contents/Resources/pythonpackages

    cp /usr/local/opt/sip/lib/python2.7/site-packages/* ./dist/Cricket.app/Contents/Resources/pythonpackages
    ditto /Library/Python/2.7/site-packages/capstone/ ./dist/Cricket.app/Contents/Resources/pythonpackages/capstone/
    ditto /Library/Python/2.7/site-packages/distorm3/ ./dist/Cricket.app/Contents/Resources/pythonpackages/distorm3/
    ditto /Library/Python/2.7/site-packages/pycparser/ ./dist/Cricket.app/Contents/Resources/pythonpackages/pycparser/

    find ./dist -type f | grep ".pyc$" | xargs rm
fi

chown -R $(whoami):staff dist/
chmod -R +w dist/

sleep 2
open ./dist/
