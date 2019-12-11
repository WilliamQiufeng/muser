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
        mkdir "$path/muser"
        cp -r dist/main.app "$path/muser/Muser.app"
        cp -r assets "$path/muser/assets"
        echo "
        "
    elif [ -f "dist/main" ]; then
        echo "Unix Copy"
        mkdir "$path/muser"
        cp -r assets "$path/muser/assets"
        cp dist/main "$path/muser/muser"
    elif [ -f "dist/main.exe" ]; then
        echo "Windows Copy"
        echo "Wait, why is this even possible to execute this in windows???"
        mkdir "$path\\Muser"
        cp -r assets "$path\\Muser\\assets"
        cp dist/main.exe "$path\\Muser\\Muser.exe"
    else
        echo "Operation System Not Found!"
    fi
fi
echo "Installation Complete."