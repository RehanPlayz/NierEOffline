import mmap
import os
import shutil
import sys

def main():
    # Define file names and offsets
    executables = {
        "NieRAutomata.exe": 0x8B6000,
        "NieRAutomataCompat.exe": 0x8AD800
    }

    original_bytes = bytes([0x33, 0xC0, 0x83])
    new_bytes = bytes([0xB0, 0x01, 0xC3])

    # Check for executables and patch the first one found
    for exe, offset in executables.items():
        if os.path.isfile(exe):
            print(f"{exe} found. Patching...")
            try:
                patch_exe(exe, offset, original_bytes, new_bytes)
            except FileNotFoundError:
                print(f"Error: File not found: {exe}")
            except PermissionError:
                print(f"Error: Permission denied for file: {exe}")
            except ValueError as ve:
                print(f"Error: {ve}")
            except Exception as e:
                print(f"Unexpected error during patching: {e}")

    print("Patching process completed.")

def patch_exe(file_path, offset, original_bytes, new_bytes):
    """
    Patches an executable file by replacing the original bytes at the given offset with new bytes.
    Creates a backup of the file before patching.
    """
    with open(file_path, 'r+b') as f:
        with mmap.mmap(f.fileno(), 0) as mm:
            # Ensure the offset is within the file bounds
            if offset + len(original_bytes) > len(mm):
                raise ValueError(f"Offset is outside the file bounds. File size: {len(mm)} bytes.")

            # Verify original bytes
            mm.seek(offset)
            current_bytes = mm.read(len(original_bytes))

            if current_bytes == new_bytes:
                print("File is already patched.")
                return

            if current_bytes != original_bytes:
                raise ValueError(
                    f"Original bytes do not match at the specified offset. "
                    f"Expected: {original_bytes.hex()}, Found: {current_bytes.hex()}"
                )

            # Backup the file before making changes
            backup_path = f"{file_path}.bak"
            shutil.copy(file_path, backup_path)
            print(f"Backup created at: {backup_path}")

            # Write the new bytes
            mm.seek(offset)
            mm.write(new_bytes)
            print("Patch applied successfully!")

if __name__ == "__main__":
    main()
