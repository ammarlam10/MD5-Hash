import binascii
import math

def rotateLeft(x, n):
    "Rotate x (32 bit) left n bits circularly."
    return (x << n) | (x >> (32-n))


st= raw_input("Input String: ")
string=bin(int(binascii.hexlify(st),16)) # convert text into binary
st=string[2:]                            # removing '0b'
binary = string[2:]
binary = binary+"1"
############# STEP 1 #####################
while len(binary)%512!=448:
    binary=binary+"0"                         #padding
############# STEP 2 ####################
append= '{0:064b}'.format(len(st))
#appending to 64 bit format
if len(append)>64:
    append=append[-64:]                                     #if greater than 64 consider lower order
low = append[-32:]
high = append[:32]
binary =binary+low+high
temp = binary
chunk=[]
i=0
while len(temp)>0:
    chunk.append(temp[:512])
    temp=temp[512:]
############# STEP 3 ####################
Ao= long('01234567',16)
Bo= long('89abcdef',16)
Co= long('fedcba98',16)
Do= long('76543210',16)
############# STEP 4 ####################

# SHIFT TABLE
s = [ 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
      4, 11, 16, 23,  4, 11, 16, 23, 4, 11,16,23,4,11,16,23,6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21, 6, 10, 15, 21]

K=[]
# Sin table
for i in range(64):
    K.append(long(math.floor(2**32*abs(math.sin(i + 1)))))

for c in chunk:  #for each 512 bit chunk
    M=[]
    temp=c
    while len(temp)>0:
        M.append(int(temp[:32],2))
        temp=temp[32:]

    A = Ao
    B = Bo
    C = Co
    D = Do
    for num in range(64):
        if  num <= 15:
            F = (B&C) | ((~B)&D)
            g = num
        elif num <= 31:
            F = (D & B) | ((~D)&C)
            g = (5*num + 1) % 16
        elif num <= 47:
            F = B^C^D
            g = (3*num + 5) % 16
        elif num <= 63:
            F = C ^ (B|(~D))
            g = (7*num)%16
        A="{0:032b}".format(A)          ## TO DEAL WITH extra bits##
        B="{0:032b}".format(B)
        C="{0:032b}".format(C)
        D="{0:032b}".format(D)
        if len(A)>32:
            A=A[-32:]
        if len(B)>32:
            B=B[-32:]
        if len(C)>32:
            C=C[-32:]
        if len(D)>32:
            D=D[-32:]
        A=long(A,2)
        B=long(B,2)
        C=long(C,2)
        D=long(D,2)                     ## TO DEAL WITH extra bits ##
        dTemp = D
        D = C
        C = B
        # total= A + F + K[num] + M[g]
        # total="{0:032b}".format(total)
        # if len(total)>32:
        #     total=total[-32:]
        # total=long(total,2)
        B=B+rotateLeft((A + F + K[num] + M[g]),s[num])
        B="{0:032b}".format(B)
        if len(B)>32:
            B=B[-32:]
        B=long(B,2)
        A = dTemp

    Ao = Ao + A
    Bo = Bo + B
    Co = Co + C
    Do = Do + D
Ao= '{0:032b}'.format(Ao)   ## TO DEAL WITH extra bits ##
Bo= '{0:032b}'.format(Bo)
Co= '{0:032b}'.format(Co)
Do= '{0:032b}'.format(Do)
if len(Ao)>32:
    Ao=Ao[-32:]
if len(Bo)>32:
    Bo=Bo[-32:]
if len(Co)>32:
    Co=Co[-32:]
if len(Do)>32:
    Do=Do[-32:]         ## TO DEAL WITH extra bits ##

digest = Ao + Bo+ Co + Do
print "Hash Value: {}".format(hex(int(digest, 2)))
print "Number of bits: {}".format(len(digest))


