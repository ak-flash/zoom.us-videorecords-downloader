@rem Build python file to exe by pyinstaller!
 
@echo off
 
echo Don`t forget to install pyinstaller and download UPX compressor!
pyinstaller take_records.py --onefile --upx-dir=upx-3.96-win64\ --console
pause