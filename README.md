# Chaos2
C&amp;C written in Python3


### Requisites
  - Wine
    ```bash
    sudo apt-get install wine
    wget https://www.python.org/ftp/python/2.7.9/python-2.7.9.amd64.msi
    wine msiexec /i python-2.7.9.amd64.msi /qb
    cd ~/.wine/drive_c/Python27
    wine python.exe Scripts/pip.exe install pyinstaller
    ```
    
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
  



