import turbofastcrypto # The source code for this module is only available for part 2 of this challenge :)
while 1:
    plaintext = input('> ')
    ciphertext = turbofastcrypto.encrypt(plaintext)
    print('Encrypted: ' + str(ciphertext))
