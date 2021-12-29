# TaiYang IT Solution (Part 1) [500|470]

**13 solves**

TaiYang IT Solution offers a variety of services, including one that is put behind a ***supposedly*** secure Google Log In. However, I heard that it uses... ***questionable*** validation code.

Log in as the admin, and get the flag! Challenge is here: http://challs.sieberrsec.tech:30593/

Source provided: http://dl.sieberrsec.tech/608fe2851fbf907e0b15c2cecdad5316886013b8581446af879ccaf6/sctf2021-jwt.7z

You'll need 7zip to open the archive. If you don't have it, [download it](https://www.7-zip.org/download.html).

## Hints
 * Open your browser's Developer Tools!
 * There are more easily-bypassable "security" measures hidden in the portal than the code might suggest.

# TaiYang IT Solution (Part 2) [900|895]

**4 solves**

After the initial vulnerability disclosure, TaiYang IT Solution employed a new cybersecurity specialist to secure their systems which used Google Sign-In.

They were complaining about how their support staff would just login with the company Google Account to any website they received in their Inbox! How terrible!

Challenge is here (part 2!): http://challs.sieberrsec.tech:30593/
(see Admin Panel Modern)

*This challenge may require you to setup a Google Firebase Project.*

*This challenge may require you to send emails (you could use Gmail, or Outlook, anything really).*

Source provided: http://dl.sieberrsec.tech/608fe2851fbf907e0b15c2cecdad5316886013b8581446af879ccaf6/sctf2021-jwt.7z

^ source is slightly modified from original

**A first blood prize of one (1) $10 GrabGifts Card is available for this challenge.**

_Author: theo_

# Notes
The `firebaseConfig` variables in all challenge files have been scrubbed to prevent abuse. Please replace those with your own Firebase Configurations.

Strictly speaking, the **JWT verification should only accept the keys listed at https://www.googleapis.com/robot/v1/metadata/x509/securetoken@system.gserviceaccount.com** (see https://firebase.google.com/docs/auth/admin/verify-id-tokens#verify_id_tokens_using_a_third-party_jwt_library). However, to give players more options, **the keys from Google's non-Firebase-specific method** were **also accepted**. **In an actual app, this would not be the case.**
