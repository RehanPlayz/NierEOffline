# NieR: Automata Offline Patch Tool

A Python tool to patch NieR: Automata's executable files to enable **Ending E** while offline.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

## 🎮 What This Does

NieR: Automata's true ending (Ending E) normally requires an online connection to display messages from other players. This tool patches the game executable to bypass that requirement, allowing you to experience the complete ending offline.

## ✨ Features

- **Automatic Detection**: Finds and patches both DirectX 11 and DirectX 12 versions
- **Safe Patching**: Creates automatic backups before making any changes
- **Flexible Options**: Command-line interface with multiple operation modes
- **Dry Run Mode**: Preview changes without actually modifying files
- **Restore Function**: Easy restoration from backup files
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 📋 Supported Executables

| File | Version | Offset |
|------|---------|--------|
| `NieRAutomata.exe` | DirectX 12 | `0x8B6000` |
| `NieRAutomataCompat.exe` | DirectX 11 Compatibility | `0x8AD800` |

## 🚀 Quick Start

### Method 1: Using Python Script (Recommended)

1. **Download the script** to your NieR: Automata game directory
2. **Run the patcher**:
   ```bash
   python NierPatch.py
   ```

That's it! The tool will automatically:
- Find your game executables
- Create backups
- Apply the necessary patches
- Verify the changes

### Method 2: Using Prebuilt Executable

1. Download the compiled `NierPatch.exe`
2. Place it in your NieR: Automata game directory
3. Run the executable
4. Follow the on-screen instructions

## 🛠️ Advanced Usage

### Command Line Options

```bash
python NierPatch.py [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `-v, --verbose` | Enable detailed output |
| `--dry-run` | Preview changes without applying them |
| `--target EXECUTABLE` | Patch only the specified executable |
| `--directory DIR` | Specify game directory (default: current) |
| `--restore` | Restore from backup files |
| `--status` | Check patch status of executables |
| `--version` | Show version information |

### Examples

```bash
# Check patch status
python NierPatch.py --status

# Preview changes without applying
python NierPatch.py --dry-run --verbose

# Patch only DirectX 12 version
python NierPatch.py --target NieRAutomata.exe

# Restore original files from backup
python NierPatch.py --restore

# Patch files in a different directory
python NierPatch.py --directory "C:\Games\NieR Automata"
```

### Status Output

The `--status` command shows the current state of your executables:

```
Patch Status:
--------------------------------------------------
✅ NieRAutomata.exe: PATCHED
❌ NieRAutomataCompat.exe: UNPATCHED
```

- ✅ **PATCHED**: Ready for offline Ending E
- ❌ **UNPATCHED**: Original, requires online connection
- ⚠️ **UNKNOWN**: Unexpected bytes found (proceed with caution)
- 💥 **INVALID_OFFSET**: File structure doesn't match expected format

## 🔧 Requirements

- **Python 3.6+** (for running the script)
- **NieR: Automata** installed on your system
- **Write permissions** to the game directory

### Python Dependencies

The script uses only built-in Python libraries:
- `mmap` - Memory-mapped file access
- `os` / `pathlib` - File system operations
- `shutil` - File copying and backup
- `argparse` - Command-line interface

## 🔒 Safety Features

### Automatic Backups
Before any modification, the tool creates backup files:
- `NieRAutomata.exe.bak`
- `NieRAutomataCompat.exe.bak`

### Verification Checks
- Confirms original bytes before patching
- Verifies patch application after modification
- Detects already-patched files to prevent double-patching

### Error Handling
- Graceful handling of permission errors
- Clear error messages for troubleshooting
- Safe restoration from backups

## 🚨 Troubleshooting

### Common Issues

**"Permission denied" error**
- Run as administrator (Windows) or with `sudo` (Linux/macOS)
- Close NieR: Automata before patching

**"File not found" error**
- Ensure you're in the correct game directory
- Verify NieR: Automata is properly installed

**"Original bytes do not match" error**
- Your game version might be different than expected
- Try updating to the latest game version
- Use `--status` to check current file state

**Patch appears successful but ending still requires internet**
- Restart the game completely
- Verify patch status with `--status` command
- Ensure you patched the correct executable version

### Manual Restoration

If something goes wrong, you can manually restore:

```bash
# Restore from backup
copy NieRAutomata.exe.bak NieRAutomata.exe
copy NieRAutomataCompat.exe.bak NieRAutomataCompat.exe
```

Or use the built-in restore function:
```bash
python NierPatch.py --restore
```

## 📖 Technical Details

### What the Patch Does

The patch modifies a single assembly instruction:

| Original | Patched | Effect |
|----------|---------|--------|
| `33 C0 83` | `B0 01 C3` | Changes function return value from 0 to 1 |

This simple change tricks the game into thinking it has received online messages, allowing Ending E to proceed offline.

### File Offsets

The patch locations were determined through reverse engineering:
- **NieRAutomata.exe**: Offset `0x8B6000`
- **NieRAutomataCompat.exe**: Offset `0x8AD800`

## 🎯 Development

### Building from Source

```bash
# Clone the repository
git clone https://github.com/RehanPlayz/NierEOffline.git
cd NierEOffline

# Run directly
python NierPatch.py

# Or build executable with PyInstaller
pip install pyinstaller
pyinstaller --onefile --name NierPatch NierPatch.py
```

### Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📜 Credits

**Massive thanks to [Lance McDonald](https://twitter.com/manfightdragon)** for discovering this solution and sharing it publicly. His original findings on [X/Twitter](https://x.com/manfightdragon/status/1700780120775291189) made this tool possible.

Lance's work involved:
- Reverse engineering the game's online connectivity checks
- Identifying the exact memory locations to patch
- Sharing the technical details with the community

This tool simply automates the manual hex editing process Lance described, making it accessible to more players.

## ⚖️ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

The MIT License allows you to:
- ✅ Use the software for any purpose
- ✅ Modify and distribute the software
- ✅ Include in commercial projects
- ❌ Hold the authors liable for any damages

---

*"Everything that lives is designed to end."* 
