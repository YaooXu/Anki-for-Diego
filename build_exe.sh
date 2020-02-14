rm -r ./build ./dist
pyinstaller runanki
cp test.db dist/runanki
cp -r web dist/runanki
