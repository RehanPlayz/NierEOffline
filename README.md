# NierEOffline
Python script to patch Nier: Automata's executable to achieve Ending E while offline.

## **Features**
- Automatically creates a backup of the original `.exe` file (`.bak` format).
- Verifies the original bytes before applying the patch.
- Supports both the DirectX 12 (`NieRAutomata.exe`) and DirectX 11 (`NieRAutomataCompat.exe`) executables.

## **Usage Instructions**

### Using the Prebuilt Executable:
1. Place the exe (`NierPatch.exe`) in the same folder as the game's executable (`NieRAutomata.exe` and/or `NieRAutomataCompat.exe`).
2. Run the exe.
3. The tool will create a backup (`NieRAutomata.exe.bak` and/or `NieRAutomataCompat.exe.bak`) and apply the patch.
4. Launch Nier: Automata and enjoy Ending E offline!

### Using the Python Script:
1. Ensure Python is installed on your system.
2. Place the script in the same folder as the game's executable (`NieRAutomata.exe` and/or `NieRAutomataCompat.exe`).
3. Run the script:
   ```bash
   python NierPatch.py
   ```
4. The tool will create a backup (`NieRAutomata.exe.bak` and/or `NieRAutomataCompat.exe.bak`) and apply the patch.
5. Launch Nier: Automata and enjoy Ending E offline!

## Credits
All credits go to Lance McDonald for his discovery and work on enabling Nier Automata's true ending [E] to be experienced offline. Lance shared the solution publicly on [X/Twitter](https://x.com/manfightdragon/status/1700780120775291189), where he explained how to patch the game by manually editing the hex value at `0x8B6000` to `B0 01 C3` (previously `33 C0 83`).
Additionally, I found the offset for `NieRAutomataCompat.exe` (`0x8AD800`) based on Lance's work, replicating the process to support this version as well.

This script automates that process, simplifying the steps for users by applying the patch automatically, eliminating the need for manual hex editing.

