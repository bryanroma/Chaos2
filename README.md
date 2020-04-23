# Chaos2
C&amp;C written in Python3

Available payloads: 
  - Linux
    - python3
    - python2
  - Windows
    - python2
    

Windows:
  - Generate payload, and execute .exe in victim.
  
Linux:
  - Run python3 payload.py
  - Done. LOL.
  
```
    # We need to compile using wine bruuuuhhhhh, :()
    # $ sudo apt-get install wine
    # $ wget https://www.python.org/ftp/python/2.7.9/python-2.7.9.amd64.msi
    # $ wine msiexec /i python-2.7.9.amd64.msi /qb
    # $ sudo dpkg --add-architecture i386 && sudo apt-get update && sudo apt-get install wine32
    # $ cd ~/.wine/drive_c/Python27
    # $ wine python.exe Scripts/pip.exe install pyinstaller
    # $ wine ~/.wine/drive_c/Python27/Scripts/pyinstaller.exe --onefile helloworld.py
```

```
# ALTERNATIVES TO pyinstaller
# CHECK :  https://anthony-tuininga.github.io/cx_Freeze/
# CHECK : https://nuitka.net/
```
