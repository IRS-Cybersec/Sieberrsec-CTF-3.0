# Turbo Fast Crypto II [900|900]
Using the key you extracted, we found a [link](.) to the source code for turbofastcrypto. There happens to be a secret flag file on the server, and you need to extract it.

**A first blood prize of one (1) month of Discord Nitro is available for this challenge**, as determined by public vote.

(the target server is the same as part 1)

_Author: @main_

## Hints
 * find a way to execute print_flag()
 * you will probably want some kind of disassembler/debugger for this. Googlable software: Binary Ninja, Ghidra, gdb

The challenge service running is `tfc.py`. It imports the `turbofastcrypto` library from the long `turbofastcrypto-cpython....so` file. `turbofastcrypto.c` is the source code for said library, and you can compile it yourself (along with any changes you wish to insert) using `./compile.sh`.

