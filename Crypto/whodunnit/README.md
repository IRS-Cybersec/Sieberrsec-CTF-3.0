# whodunnit [900|895]
The Association of Criminals, Subversives and Insurgents (ACSI, in short) are big fans of [RSA encryption](https://en.wikipedia.org/wiki/RSA_(cryptosystem)), and recently published a [list of their members' public keys](Suspicious_List.csv). For reasons unbeknownst to us, they have a habit of **signing** their messages with **multiple** private keys before **encrypting** the signed message with a **single** public key.

Using one of our portable False Base Stations, we [captured](interception.txt) one of ASCI's **encrypted**, **doubly-signed**, super secret **alphabetic** passwords (along with the public key used to encrypt it). We need you to figure out **who signed the password**, and **what the password** is by decrypting && unsigning the captured RSA transmission.

Flag format: `IRS{Name of first person to sign_Name of second person to sign_The password}`

_Challenge description extemporised by @main_

_Author: @syralie_

## Hints
 * \[Encryption: M^e % n = C\] \[Decryption: C^d % n = M\] \[Signing: M^d % n = S\] \[Unsigning S: S^e % n = M\]
 * Obtaining a decryption key (d) is not necessary at any point in this challenge.
 * try to read the bolded words
