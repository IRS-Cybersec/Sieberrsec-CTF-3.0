import base64
flag = open("flag.jpg", "rb").read()
key = int(open("key.txt", "r").read())
flag = base64.b64encode(flag)
flag = flag.decode('ascii')
digits = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/="
encrypted = ""
for c in flag:
    cur = (digits.find(c) + key) % 65
    if(cur < 10):
        encrypted = encrypted + '0' + str(cur)
    else:
        encrypted = encrypted + str(cur)
f = open("flag.jpg.encrypted", "w")
f.write(encrypted)
f.close()