# turbofastcrypto [150|117]
We found the frontend code for a remote encryption service at  `nc challs.sieberrsec.tech 3477`:

```python
import turbofastcrypto # The source code for this module is only available for part 2 of this challenge :)
while 1:
    plaintext = input('> ')
    ciphertext = turbofastcrypto.encrypt(plaintext)
    print('Encrypted: ' + str(ciphertext))
```

My partner says it operates under the hood with "[XOR](https://en.wikipedia.org/wiki/Exclusive_or)", whatever that means. I need you to recover the key.

_Author: @main_

## Hints
 * Reset the connection if you're having trouble.

## Note
The server files for this challenge are located under the Pwn folder [here](../../Pwn/turbofastcrypto). The flag for this challenge is `IRS{secrets_are_revealed!!}`.

