# rock_farming_simulator
Connect with `ssh -p 15233 rock_farming_simulator@irscybersec.tk`.

The following command is executed on the remote server when you connect: `timeout 100 stdbuf -i0 -o0 /home/rock_farming_simulator/rockfarming_simulator`.

`ssh` is solely used here to allocate a pseudo-tty to make the ncurses-based service work properly.
**There is no ssh jailbreak, Linux pentesting, username bruteforcing, etc.** involved in this challenge.
If you waste your time doing so, it will be considered an attack on server infrastructure && consequently a valid reason for disqualification.

# Running the challenge locally
Although I have provided the challenge binary itself, you may have reasons to compile the challenge on your own machine. As `src.tar.gz` shows, this challenge was written in the Rust programming language. If you are not familiar with it, I suggest reading [the first chapter of the Rust Book](https://doc.rust-lang.org/stable/book/ch01-01-installation.html) if you want to compile and run the program with debug mode enabled.

If you aren't in the mood for reading, then the short answer is:

1. `curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh`
2. `rustup override set nightly`
3. `cargo run`

# Other info
`rock_farming_simulator` was designed by @main, with assistance from @willi123yao in getting ssh configured right.
