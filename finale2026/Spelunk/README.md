# Write-up : Spelunk (Catégorie Pwn)

## 1. Analyse Initiale (Reconnaissance)

L'énoncé fournissait le code source `spelunk.c` et son `Makefile`. L'analyse de ces fichiers nous a donné deux informations cruciales :

- **Les protections sont désactivées :** Le `Makefile` indiquait `fno-stack-protector` (pas de protection contre les débordements) et `z execstack` (la pile est exécutable). Cela signifie qu'on peut injecter notre propre code dans la mémoire et forcer le programme à l'exécuter (technique du *Ret2Shellcode*).
- **Le secret des File Descriptors (FD) :** Le code source montrait que le programme ouvre le fichier du flag (`/tmp/flag.txt`) dès son lancement. Puisque `stdin(0)`, `stdout(1)` et `stderr(2)` sont occupés, ce fichier prend logiquement le **Descripteur de Fichier 3 (FD 3)**.

## 2. La Vulnérabilité (Le point d'entrée)

La fonction `vuln()` présentait deux failles majeures :

1. **Un Leak d'adresse :** Le programme affichait volontairement l'adresse mémoire de notre variable `buf` via la ligne `printf("I can see my map at: %p\n", (void *)buf);`.
2. **Un Buffer Overflow :** Le programme utilisait la fonction `gets(buf)` pour lire notre entrée. `gets()` est tristement célèbre car elle ne limite pas la taille de la lecture. En envoyant plus de 128 octets, on pouvait déborder du buffer et écraser les registres de contrôle du programme, notamment `EIP` (Instruction Pointer), qui dit au processeur quelle est la prochaine instruction à exécuter.

## 3. La Stratégie d'Exploitation (Le Shellcode)

Dans un pwn classique, on injecte un shellcode qui ouvre un terminal (`/bin/sh`). Ici, ça n'aurait pas fonctionné car nos entrées/sorties étaient redirigées vers une socket réseau (`dup2`).

La stratégie a donc été de forger un **Shellcode personnalisé** :

- **Étape A :** Utiliser l'appel système `read` pour lire 100 octets depuis le FD `3` (le fichier du flag ouvert) et les stocker temporairement sur la pile (`esp`).
- **Étape B :** Utiliser l'appel système `write` pour prendre ces 100 octets sur la pile et les envoyer vers le FD `1` (notre connexion réseau).

## 4. L'Ajustement Final (Le "Address Spraying")

Lors du premier essai, le script a fait crasher le serveur (erreur `EOF`). Cela arrive quand on se trompe de quelques octets sur l'endroit exact où se trouve `EIP` (l'offset).

Pour fiabiliser l'exploit sans avoir à chercher l'offset exact sur le serveur distant, nous avons utilisé une technique agressive :

- **Le NOP Sled :** Nous avons rempli l'espace vide après notre shellcode avec des octets `\x90` (NOP - No Operation). Si le processeur atterrit n'importe où là-dedans, il "glisse" jusqu'au shellcode.
- **Le Spam d'EIP :** Au lieu de mettre l'adresse de retour (le leak) une seule fois à la position 132, nous l'avons multipliée 10 fois pour écraser une large zone de la mémoire (de 120 à 160 octets). Peu importe où se trouvait exactement `EIP`, il a été écrasé par la bonne adresse.

## 5. Résultat

En envoyant ce "payload" (charge utile), le programme a terminé la fonction `vuln()`, a lu notre fausse adresse de retour, a sauté dans notre shellcode, a lu le fichier 3, et nous l'a renvoyé à l'écran !

*(Note : Les caractères bizarres `\x00\x00\x00...` que tu vois à la fin de ton terminal sont normaux. C'est simplement parce que notre shellcode a lu "100 octets" en tout. Une fois le flag de 47 caractères lu, il a continué à lire la "poubelle" présente dans la mémoire juste après le flag, et te l'a affichée).*
