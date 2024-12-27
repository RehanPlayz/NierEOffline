import mmap
import os
import shutil
import sys

def patch_exe(file_path, offset, original_bytes, new_bytes):
    try:
        # Backup the file before making changes
        backup_path = f"{file_path}.bak"
        shutil.copy(file_path, backup_path)
        print(f"Backup created at: {backup_path}")

        with open(file_path, 'r+b') as f:
            mm = mmap.mmap(f.fileno(), 0)

            # Ensure the offset is within the file bounds
            if offset + len(original_bytes) > len(mm):
                print("Error: Offset is outside the file bounds.")
                return

            # Verify original bytes
            mm.seek(offset)
            current_bytes = mm.read(len(original_bytes))

            if current_bytes != original_bytes:
                print("Error: Original bytes do not match at the specified offset.")
                print(f"Expected: {original_bytes.hex()}, Found: {current_bytes.hex()}")
                return

            # Write the new bytes
            mm.seek(offset)
            mm.write(new_bytes)
            print("Patch applied successfully!")
            mm.close()

    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
    except PermissionError:
        print(f"Error: Permission denied for file: {file_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Specify the file path
    exe_path = "NieRAutomata.exe"  
    if not os.path.isfile(exe_path):
        print(f"Error: File does not exist: {exe_path}")
        sys.exit(1)

    offset = 0x8B6000
    original_bytes = bytes([0x33, 0xC0, 0x83])
    new_bytes = bytes([0xB0, 0x01, 0xC3])

    patch_exe(exe_path, offset, original_bytes, new_bytes)
