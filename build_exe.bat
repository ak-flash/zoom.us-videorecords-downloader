@rem Build python file to exe by pyinstaller!
 
@echo off
 
echo Don`t forget to install pyinstaller!
pyinstaller take_records.py --onefile --console
pause