
Instructions for Mac (already includes Python 2.7)

1. Install pip (Python Package Index)
sudo easy_install pip


2. Install pillow
sudo pip install pillow

3. Run the script

python pyflash.py %FOLDER_TO_SCAN%


Instructions for Windows (Tested with Windows 8.1 Pro)

NOTE: you can avoid using the full path to the Python install for every command by adding the folder to your PATH

1. Install latest Python 2 to Windows
https://www.python.org/downloads/windows/

(Tested with Python 2.7.10)

Open command window and confirm python version:
c:\%PYTHON_LOCATON%\python.exe -v

at the bottom of output it should say something like:
Python 2.7.10 (default, May 23 2015, 09:44:00) [MSC v.1500 64 bit (AMD64)] on win32

To exit Python command line type:

exit()

Then press Enter

2. Install pillow extension

C:\%PYTHON_LOCATION%\Scripts\pip.exe install pillow

3. Run script:
c:\%PYTHON_LOCATION%\python.exe pyflash.py %FOLDER_TO_SCAN%




