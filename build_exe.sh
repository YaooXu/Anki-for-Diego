rm -r ./build ./dist
pyinstaller runanki
cp test.db dist/runanki
cp -r web dist/runanki
cp -r local dist/local
cp stdfield.json dist/stdfield.json