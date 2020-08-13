# Expressive Eyes


## To install/use on the Jolla phone

- SSH on the phone
- `cd /media/sdcard/7318-A0DD/src/expressive-eyes` (clone the repo first if needed)
- `git pull`
- `python3 setup.py install --user`

The first time, you need to install the app to make it accessible from the shell:
- `ln -s /media/sdcard/7318-A0DD/src/expressive-eyes /usr/share/expressive_eyes`
- `cp qml/expressive-eyes.desktop /usr/share/applications/`
- `cp qml/expressive_eyes.png /usr/share/icons/hicolor/86x86/apps/`
