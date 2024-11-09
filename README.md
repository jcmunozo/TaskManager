# TaskManager
A task manager to manage daily routines

---

## Technologies

- [PyQt6](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [SQLite](https://www.sqlite.org/)

---

## How to start

create a env with:
```
python3 -m venv env
```
activate the env with:
```
source env/bin/activate
```
run the main file with:
```
python main.py
```

## Create an executable

I'm using the library pyinstaller so you can run this:
```
pyinstaller --onefile --windowed main.py
```
Then of this you have a folder called dist/ and within it our .exe file

## Fedora aplication directory

You can create a .desktop file:
```
nvim ~/.local/share/applications/taskmanager.desktop
```
add this in it:
```
[Desktop Entry]
Name=TaskManager
Comment=A task manager writen in PyQt6
Exec=/path/to/ejecutable/main  # Change it to your path
Icon=/path/to/icono.png        # Change it to your path
Terminal=false
Type=Application
Categories=Utility;            # Other categories could be: Development; Productivity;

```
Once this is done, your application should appear in the Fedora applications menu.

---
