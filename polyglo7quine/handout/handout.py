import subprocess
import base64
import tempfile

"""
NOTE: This is not the file that is being run on remote. This is only being provided for convenience.

To make the challenge as cheese-proof as possible, the real source code will not be provided.
I didn't want to have people guessing though, so I have provided this handout as a tester for your code.

If your solution **does not use any cheese strats** and works on this handout, then it should work on remote.
If it does not work on remote, open a ticket, ping @oh_word, and send your code.

For clarification, an example cheese strat would be reading the source code written on disk and printing it out.
It may work in this handout, but it will not work on remote.

Finally, here are all the versions for all the languages:
Python 3.10.12
Ruby 3.0.2p107
Perl v5.34.0
Lua 5.3.6
PHP 8.1.2
gcc/g++ version 11.4.0

Good luck
"""

code = base64.b64decode(input("Base64 encoded code > "))

def runner(args, language):
    global code
    TIMEOUT = 2.0

    try:
        # only stdout matters, if anything gets output to stderr it will be ignored
        proc = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=TIMEOUT)

        if proc.returncode != 0:
            raise subprocess.CalledProcessError
        
        # checks for full equality, beware of rogue newlines in your output
        assert proc.stdout == code
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to run {language} code")
    except subprocess.TimeoutExpired:
        print(f"{language} code timed out")
    except AssertionError:
        print(f"{language} quine check failed")
    except Exception as e:
        print(f"Unknown exception: {e}")

    return False

with tempfile.TemporaryDirectory() as temp_dir:
    prg = tempfile.NamedTemporaryFile(delete=False)
    prg.write(code)
    prg.close()

    filename_c = f"{temp_dir}/out_c"
    filename_cpp = f"{temp_dir}/out_cpp"

    gcc_ret = subprocess.call(["gcc", "-x", "c", "-o", filename_c, prg.name, "-w"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if gcc_ret != 0:
        print("Failed to compile C code")
        exit()
        
    gpp_ret = subprocess.call(["g++", "-x", "c++", "-o", filename_cpp, prg.name, "-w"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if gpp_ret != 0:
        print("Failed to compile C++ code")
        exit()

    if (
        runner([filename_c], "C") and \
        runner([filename_cpp], "C++") and \
        runner(["perl", prg.name], "perl") and \
        runner(["ruby", prg.name], "ruby") and \
        runner(["lua", prg.name], "lua") and \
        runner(["python3", prg.name], "python") and \
        runner(["php", prg.name], "php")
    ):
        print("You win! jail{fake_flag}")
    else:
        print("You lose!")
