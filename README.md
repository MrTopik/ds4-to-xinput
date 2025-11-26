# ds4-to-xinput
DualShock 4 to XInput with pygame and VigemBus

This program does not let you configure buttons in a simple way, I made it to just work and I don't plan to add any features.<br>
You can change the buttons if you change the code itself and then build it.

Installation

1 - Install [VigemBus](https://github.com/nefarius/ViGEmBus/releases)<br>
2 - Install [HidHide](https://github.com/nefarius/HidHide) if the game detects your controller but you want to use the virtual one.<br>
3 - Run the file and it is done

Building

1 - Install [VigemBus](https://github.com/nefarius/ViGEmBus/releases) (required) and [HidHide](https://github.com/nefarius/HidHide) (optional)<br>
2 - Install Python and add it to the PATH<br>
3 - Install modules by typing "pip install pyinstaller", "pip install pygame" and "pip install vgamepad" into a PowerShell terminal.<br>
4 - Open the path where the file exists in PowerShell and type "pyinstaller --onefile --collect-all vgamepad ds4-to-xinput.py"<br>
5 - After that is done enter dist folder and run the exe

How to use HidHide (optional)

1 - Install HidHide and open the program<br>
2 - On applications page add the ds4-to-xinput.exe<br>
3 - Click on devices page and find your controller not the virtual one<br>
4 - Select your controller and click "Enable device hiding"
