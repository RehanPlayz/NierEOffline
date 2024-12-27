# NierEOffline
Python script to patch Nier: Automata's executable to achieve Ending E while offline.

## **Features**
- Automatically creates a backup of the original `.exe` file (`.bak` format).
- Verifies the original bytes before applying the patch.

## **Usage Instructions**

### Using the Prebuilt Executable:
1. Place the tool in the same folder as the game's executable (`NieRAutomata.exe`).
2. Run the tool.
3. The tool will create a backup (`NieRAutomata.exe.bak`) and apply the patch.
4. Launch the game and enjoy!

### Using the Python Script:
1. Ensure Python is installed on your system.
2. Edit the `exe_path` variable in the script to point to your game executable.
3. Run the script:
   ```bash
   python patch_exe.py
   ```

## Credits
All credits go to Lance McDonald for his discovery and work on enabling Nier Automata's true ending [E] to be experienced offline. Lance shared the solution publicly on [X/Twitter](https://x.com/manfightdragon/status/1700780120775291189), where he explained how to patch the game by manually editing the hex value at `0x8B6000` to `B0 01 C3` (previously `33 C0 83`).

This script automates that process, simplifying the steps for users by applying the patch automatically, eliminating the need for manual hex editing.

