# TaiYang IT Solution (Part 1) [500|470]
TaiYang IT Solution offers a variety of services, including one that is put behind a ***supposedly*** secure Google Log In. However, I heard that it uses... ***questionable*** validation code.

Log in as the admin, and get the flag! Challenge is here: http://challs.sieberrsec.tech:30593/

Source provided: http://dl.sieberrsec.tech/608fe2851fbf907e0b15c2cecdad5316886013b8581446af879ccaf6/sctf2021-jwt.7z

You'll need 7zip to open the archive. If you don't have it, [download it](https://www.7-zip.org/download.html).

## Hints
 * Open your browser's Developer Tools!
 * There are more easily-bypassable "security" measures hidden in the portal than the code might suggest.

# TaiYang IT Solution (Part 2) [900|895]
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
The `firebaseConfig` variable in `login-v1.php` has been scrubbed to prevent abuse. Please replace it with your own API keys for use.
