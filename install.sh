if [ "$1" != "-n" ]; then
    echo "Building......"
    pyxelpackager main.py
    echo "Build complete."
fi
read -p "Where do you want to install this program[path/n]:" path
if [ $path == "n" ];
then
    echo "No installation"
else
    if [ -d "dist/main.app" ]; then
        echo "OSX Copy"
        cp -r dist/main.app "$path/Muser.app"
    elif [ -f "dist/main" ]; then
        echo "Unix Copy"
        cp dist/main "$path/muser"
    elif [ -f "dist/main.exe" ]; then
        echo "Windows Copy"
        echo "Wait, why is this even possible to execute this in windows???"
        cp dist/main.exe "$path\\Muser.exe"
    else
        echo "Operation System Not Found!"
    fi
fi
echo "Installation Complete."