# totallyfoolproofcrypto [900|884]
In hindsight, rolling my own crypto was a rather stupendous stroke of stupidity. I'll be switching to a [well-known, verified library](https://www.pycryptodome.org/en/latest/) to fix this.

```python
from Crypto.Util.Padding import pad,unpad
from Crypto.Cipher import AES
import os

with open("flag", 'rb') as f: flag = f.read().strip()
key = os.urandom(16)

while 1:
    pt = input('> ').encode()
    padded = pad(pt+flag, AES.block_size)
    cipher = AES.new(key, AES.MODE_ECB)
    print(cipher.encrypt(padded).hex())
```

`nc challs.sieberrsec.tech 31311`

**A first blood prize of one (1) month of Discord Nitro is available for this challenge.**

Some amount of "bruteforce" will be necessary -- and hence legal -- for this challenge.

_Author: @main`

## Hints
 * You should search for ECB related AES crypto CTF problems; this is a rather common newbie challenge
