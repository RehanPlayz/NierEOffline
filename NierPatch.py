#!/usr/bin/env python3
"""
NieR: Automata Offline Patch Tool
Patches NieR: Automata executable to enable Ending E while offline.

Based on Lance McDonald's discovery: https://x.com/manfightdragon/status/1700780120775291189
"""

import argparse
import mmap
import os
import shutil
import sys
from pathlib import Path
from typing import Dict, Optional, Tuple

# Version info
__version__ = "2.0.0"
__author__ = "RehanPlayz"

class PatchConfig:
    """Configuration for patching different NieR: Automata executables."""
    
    EXECUTABLES = {
        "NieRAutomata.exe": {
            "offset": 0x8B6000,
            "description": "DirectX 12 version"
        },
        "NieRAutomataCompat.exe": {
            "offset": 0x8AD800,
            "description": "DirectX 11 compatibility version"
        }
    }
    
    ORIGINAL_BYTES = bytes([0x33, 0xC0, 0x83])
    NEW_BYTES = bytes([0xB0, 0x01, 0xC3])
    


class PatchError(Exception):
    """Custom exception for patching errors."""
    pass

class NieRPatcher:
    """Main patcher class for NieR: Automata executables."""
    
    def __init__(self, verbose: bool = False, dry_run: bool = False):
        self.verbose = verbose
        self.dry_run = dry_run
        self.config = PatchConfig()
    
    def log(self, message: str, force: bool = False) -> None:
        """Log a message if verbose mode is enabled."""
        if self.verbose or force:
            print(f"[INFO] {message}")
    
    def error(self, message: str) -> None:
        """Print an error message."""
        print(f"[ERROR] {message}", file=sys.stderr)
    
    def warning(self, message: str) -> None:
        """Print a warning message."""
        print(f"[WARN] {message}")
    

    def create_backup(self, file_path: Path) -> Path:
        """Create a backup of the original file."""
        backup_path = file_path.with_suffix(file_path.suffix + '.bak')
        
        if backup_path.exists():
            self.log(f"Backup already exists: {backup_path}")
            return backup_path
        
        if not self.dry_run:
            try:
                shutil.copy2(file_path, backup_path)
                self.log(f"Backup created: {backup_path}", force=True)
            except Exception as e:
                raise PatchError(f"Failed to create backup: {e}")
        else:
            self.log(f"[DRY RUN] Would create backup: {backup_path}")
        
        return backup_path
    
    def check_patch_status(self, file_path: Path, offset: int) -> str:
        """Check if the file is already patched, unpatched, or unknown."""
        try:
            with open(file_path, 'rb') as f:
                with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                    if offset + len(self.config.ORIGINAL_BYTES) > len(mm):
                        return "invalid_offset"
                    
                    mm.seek(offset)
                    current_bytes = mm.read(len(self.config.ORIGINAL_BYTES))
                    
                    if current_bytes == self.config.NEW_BYTES:
                        return "patched"
                    elif current_bytes == self.config.ORIGINAL_BYTES:
                        return "unpatched"
                    else:
                        return "unknown"
        except Exception as e:
            raise PatchError(f"Failed to check patch status: {e}")
    
    def apply_patch(self, file_path: Path, offset: int) -> bool:
        """Apply the patch to the specified file."""
        try:
            # Check current patch status
            status = self.check_patch_status(file_path, offset)
            
            if status == "patched":
                self.log(f"{file_path.name} is already patched", force=True)
                return True
            elif status == "invalid_offset":
                raise PatchError(f"Offset 0x{offset:X} is outside file bounds")
            elif status == "unknown":
                current_bytes = None
                with open(file_path, 'rb') as f:
                    f.seek(offset)
                    current_bytes = f.read(len(self.config.ORIGINAL_BYTES))
                
                raise PatchError(
                    f"Unexpected bytes at offset 0x{offset:X}. "
                    f"Expected: {self.config.ORIGINAL_BYTES.hex().upper()} or {self.config.NEW_BYTES.hex().upper()}, "
                    f"Found: {current_bytes.hex().upper()}"
                )
            
            # Create backup before patching
            self.create_backup(file_path)
            
            if not self.dry_run:
                # Apply the patch
                with open(file_path, 'r+b') as f:
                    with mmap.mmap(f.fileno(), 0) as mm:
                        mm.seek(offset)
                        mm.write(self.config.NEW_BYTES)
                
                # Verify the patch was applied correctly
                if self.check_patch_status(file_path, offset) == "patched":
                    self.log(f"Patch applied successfully to {file_path.name}", force=True)
                    return True
                else:
                    raise PatchError("Patch verification failed")
            else:
                self.log(f"[DRY RUN] Would patch {file_path.name} at offset 0x{offset:X}")
                return True
                
        except Exception as e:
            if isinstance(e, PatchError):
                raise
            else:
                raise PatchError(f"Failed to patch {file_path.name}: {e}")
    
    def restore_backup(self, file_path: Path) -> bool:
        """Restore a file from its backup."""
        backup_path = file_path.with_suffix(file_path.suffix + '.bak')
        
        if not backup_path.exists():
            self.error(f"Backup not found: {backup_path}")
            return False
        
        try:
            if not self.dry_run:
                shutil.copy2(backup_path, file_path)
                self.log(f"Restored {file_path.name} from backup", force=True)
            else:
                self.log(f"[DRY RUN] Would restore {file_path.name} from backup")
            return True
        except Exception as e:
            self.error(f"Failed to restore backup: {e}")
            return False
    
    def find_executables(self, directory: Path = None) -> Dict[str, Path]:
        """Find NieR: Automata executables in the specified directory."""
        if directory is None:
            directory = Path.cwd()
        
        found_exes = {}
        for exe_name in self.config.EXECUTABLES.keys():
            exe_path = directory / exe_name
            if exe_path.is_file():
                found_exes[exe_name] = exe_path
                self.log(f"Found {exe_name} ({self.config.EXECUTABLES[exe_name]['description']})")
        
        return found_exes
    
    def patch_all(self, directory: Path = None, target_exe: str = None) -> bool:
        """Patch all found executables or a specific target."""
        if directory is None:
            directory = Path.cwd()
        
        found_exes = self.find_executables(directory)
        
        if not found_exes:
            self.error("No NieR: Automata executables found in the current directory")
            self.log("Expected files: " + ", ".join(self.config.EXECUTABLES.keys()))
            return False
        
        if target_exe:
            if target_exe not in found_exes:
                self.error(f"Specified executable not found: {target_exe}")
                return False
            found_exes = {target_exe: found_exes[target_exe]}
        
        success_count = 0
        for exe_name, exe_path in found_exes.items():
            try:
                self.log(f"Processing {exe_name}...", force=True)
                
                # Apply patch
                offset = self.config.EXECUTABLES[exe_name]["offset"]
                if self.apply_patch(exe_path, offset):
                    success_count += 1
                    
            except PatchError as e:
                self.error(f"Failed to patch {exe_name}: {e}")
            except Exception as e:
                self.error(f"Unexpected error while patching {exe_name}: {e}")
        
        if success_count > 0:
            print(f"\n✅ Successfully processed {success_count}/{len(found_exes)} executable(s)")
            if not self.dry_run:
                print("🎮 You can now enjoy NieR: Automata Ending E offline!")
            return True
        else:
            print(f"\n❌ Failed to patch any executables")
            return False

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="NieR: Automata Offline Patch Tool - Enable Ending E while offline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python NierPatch.py                    # Patch all found executables
  python NierPatch.py -v                 # Verbose output
  python NierPatch.py --dry-run          # Show what would be done
  python NierPatch.py --target NieRAutomata.exe  # Patch specific executable
  python NierPatch.py --restore          # Restore from backup
  python NierPatch.py --status           # Check patch status

Credits: Lance McDonald (@manfightdragon) for the original discovery
        """
    )
    
    parser.add_argument("-v", "--verbose", action="store_true",
                       help="Enable verbose output")
    parser.add_argument("--dry-run", action="store_true",
                       help="Show what would be done without making changes")
    parser.add_argument("--target", metavar="EXECUTABLE",
                       help="Target specific executable to patch")
    parser.add_argument("--directory", metavar="DIR", type=Path,
                       help="Directory containing the executables (default: current)")
    parser.add_argument("--restore", action="store_true",
                       help="Restore executables from backup files")
    parser.add_argument("--status", action="store_true",
                       help="Check patch status of found executables")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    
    args = parser.parse_args()
    
    # Create patcher instance
    patcher = NieRPatcher(verbose=args.verbose, dry_run=args.dry_run)
    
    try:
        if args.status:
            # Check status of all found executables
            found_exes = patcher.find_executables(args.directory)
            if not found_exes:
                patcher.error("No NieR: Automata executables found")
                return 1
            
            print("Patch Status:")
            print("-" * 50)
            for exe_name, exe_path in found_exes.items():
                offset = patcher.config.EXECUTABLES[exe_name]["offset"]
                status = patcher.check_patch_status(exe_path, offset)
                status_emoji = {"patched": "✅", "unpatched": "❌", "unknown": "⚠️", "invalid_offset": "💥"}
                print(f"{status_emoji.get(status, '❓')} {exe_name}: {status.upper()}")
            
        elif args.restore:
            # Restore from backups
            found_exes = patcher.find_executables(args.directory)
            if not found_exes:
                patcher.error("No NieR: Automata executables found")
                return 1
            
            success_count = 0
            for exe_name, exe_path in found_exes.items():
                if patcher.restore_backup(exe_path):
                    success_count += 1
            
            print(f"Restored {success_count}/{len(found_exes)} executable(s) from backup")
            
        else:
            # Normal patching operation
            success = patcher.patch_all(args.directory, args.target)
            return 0 if success else 1
            
    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user")
        return 1
    except Exception as e:
        patcher.error(f"Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
