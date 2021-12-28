from csv import reader
from gmpy2 import cbrt
from itertools import permutations
with open('Suspicious_List.csv') as f:
    sus = {l[0]: [int(v) for v in l[1:]] for l in list(reader(f))[1:]}
c = 219299933729115529784559411697089963323
S = int(cbrt(c))
def design(e1,n1,e2,n2):
    return pow(pow(S,e1,n1),e2,n2).to_bytes(99,'big').strip(b'\0')
n1,n2 = next((p2,p1) for p1,p2 in permutations(sus,2)\
        if design(*(sus[p1]+sus[p2])).isalpha())
print("IRS{%s_%s_%s}" % (n1,n2,design(*(sus[n2]+sus[n1])).decode()))
