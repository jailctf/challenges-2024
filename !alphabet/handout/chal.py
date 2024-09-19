#!/usr/local/bin/python3 -u
import os
import subprocess
import tempfile
import re

print("Input your code (1 line)")
code = input("> ")

if re.search(r'[A-Za-z]', code):
    print("No letters allowed")
    exit(1)

with tempfile.TemporaryDirectory() as td:
    src_path = os.path.join(td, "source.c")
    compiled_path = os.path.join(td, "compiled")
    with open(src_path, "w") as file:
        file.write(code)
    
    # Entry point is _ *NOT* main. Keep that in mind
    # as the chal is literally impossible without this
    returncode = subprocess.call(["gcc", "-B/usr/bin", "-Wl,--entry=_", "-nostartfiles", "-w", "-O0", "-o", compiled_path, src_path], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

    if returncode != 0:
        print("Oops, there were some compilation errors!")
        exit(1)

    print("Good luck!")
    subprocess.call([compiled_path])