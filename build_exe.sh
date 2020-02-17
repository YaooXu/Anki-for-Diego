rm -r ./build ./dist
pyinstaller -w runanki
cp test.db dist/runanki
cp -r web dist/runanki
cp -r locale dist/runanki
cp stdfield.json dist/runanki