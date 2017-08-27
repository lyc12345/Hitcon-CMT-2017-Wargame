from pwn import *
import base64,string
de = base64.b64decode
en = base64.b64encode

letter = map(chr,range(32,127))

def xor(a,b):
    c = [chr(ord(a[i])^ord(b[i])) for i in xrange(len(a))]
    return ''.join(c)

r = remote('pwnhub.tw',12345)
wel = de(r.recvline())
assert len(wel) == 32
iv = wel[:16]
wel = wel[16:]

plain = 'Welcome!!'+'\x07'*7
target = 'get-flag'+'\x08'*8
iv = xor(iv,plain)
iv = xor(iv,target)
#iv = iv[:-2]+'\x00'+iv[-1]

msg = en(iv+wel)

r.sendline(msg)
magic = r.recvline().strip()
msg = de(magic)
iv = msg[:16]
msg = msg[16:]

tmagic = magic
print magic
flag = 'hitcon{'
target = 'get-flag'
for offset in xrange(8,17):
    for c in letter:
        iv1 = xor(iv[:offset],target)
        p = flag+c
        iv1 = xor(iv1,p)
        iv1 = iv1+iv[offset:]
        r.sendline(en(iv1+msg))
        res = r.recvline().strip()
        if res == magic:
            flag += c
            target = ' '+target
            offset += 1
            break
    print flag
    if flag[-1] == '}': break


iv1 = xor(iv[:4],'echo')
iv1 = xor(iv1,'hitc')
iv1 = iv1+iv[4:]
msg = en(iv1+msg)
r.sendline(msg)
magic = r.recvline().strip()
msg = de(magic)
iv = msg[:16]
msg = msg[16:]
iv1 = xor(iv[:4],'echo')
iv1 = xor(iv1,flag[4:8])
iv1 = iv1+iv[4:]
msg = en(iv1+msg)
r.sendline(msg)
magic = r.recvline().strip()
flag_1 = flag[:8]
flag = flag[8:15]
msg = de(magic)
iv = msg[:16]
msg = msg[16:]

target = 'get-flag'
for offset in xrange(8,17):
    for c in letter:
        iv1 = xor(iv[:offset],target)
        p = flag+c
        iv1 = xor(iv1,p)
        iv1 = iv1+iv[offset:]
        r.sendline(en(iv1+msg))
        res = r.recvline().strip()
        if res == tmagic:
            flag += c
            target = ' '+target
            offset += 1
            break
    print flag_1+flag
    if flag[-1] == '}': break
r.interactive()
