import os
import sys

with open("test_log.txt", "w") as f:
    f.write("Test write successful\n")
    f.write(f"CWD: {os.getcwd()}\n")
    try:
        import openpyxl
        f.write("openpyxl imported successfully\n")
    except ImportError as e:
        f.write(f"openpyxl import failed: {e}\n")
