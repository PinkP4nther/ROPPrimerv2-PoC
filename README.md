# ROPPrimerv2-PoC
My ROPPrimer v2 Proof of Concepts

level0: I messed around with this level a lot at first I had a ROP chain going of about 3 calls added into memory but got it down to one call that returns to shellcode by leveraging the mapped memory segment. I was able to leverage it because my buffer is written to it when the call to gets() reads in my payload. I then take advantage of a crash to initiate a ROP sequence. I call mprotect and make the mapped section of memory RWX then return to the shellcode that was placed on the mapped segment from the gets() call earlier. Shell popped!

level1: For this level I chose to shake it up and instead of getting a shell I read the flag. I used 3 links in my ROP chain the first ROP to the open call to open the flag file. The second ROP to the read call to read the file onto the stack. Finally the third ROP to the write call to write the flag buffer placed on the stack (52 bytes) to the file descriptor for the socket within the binary causing the flag to be sent over the connection to my machine.
