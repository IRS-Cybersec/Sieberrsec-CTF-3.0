import base64
flag = open("flag.txt", "rb").read()
flag = base64.b64encode(flag)
flag = flag.decode('ascii')
digits = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/="
encrypted = ""
for c in flag:
    cur = digits.find(c)
    if(cur < 10):
        encrypted = encrypted + '0' + str(cur)
    else:
        encrypted = encrypted + str(cur)
f = open("flag.txt.encrypted", "w")
f.write(encrypted)
f.close()