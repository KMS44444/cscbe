## Grandma's Beautiful Scarf

## Description

```text
My grandmother was a woman of two passions: knitting and "keeping secrets from the neighbors." 
She sent me this 10x10 embroidery pattern and a scrap of paper with some odd knitting instructions. 
She said, "If you follow the stitches and keep turning the cloth, the truth will come out in the wash." 
Can you help grandma make a beautiful scarf ?
```

**Catégorie :** Cryptographie / Stéganographie

**Concept :** Grille tournante (Fleissner Grille)

## Write-up

### 1. Analyse de l'énoncé

L'énoncé nous donne deux indices cruciaux :

- **"10x10 embroidery pattern"** : Un carré de 100 caractères (notre texte chiffré).
- **"Keep turning the cloth"** : Indice direct vers une **grille tournante**, une technique de chiffrement par transposition où une grille percée de trous est pivotée pour révéler des lettres.
- **"Knitting instructions"** : Une suite de `Knit` (Mailles endroit) et `Purl` (Mailles envers). En cryptographie "maison", cela correspond souvent à un flux binaire ou, dans ce cas précis, à la position des trous dans la grille.

### 2. Déchiffrement des instructions

Pour construire la grille de lecture, nous traduisons les instructions de tricot en positions numériques (de 0 à 99) :

- **Knit X** : On perce **X** trou(s) à la position actuelle.
- **Purl X** : On saute **X** case(s) sans percer.

**Calcul des positions (0-indexed) :**

‎1. `Knit 1` : Position **0**

‎2. `Purl 4` : Saute 1, 2, 3, 4 $\rightarrow$ Prochaine position : **5**

‎3. `Knit 1` : Position **5**

‎4. `Purl 15` : Saute 15 cases $\rightarrow$ Prochaine position : **21**

‎5. ... et ainsi de suite.

Les trous initiaux (Rotation 0°) se situent donc aux index : `[0, 5, 21, 27, 43, 62, 88, 89]`.

### 3. La Théorie : Rotation de Grille

Pour une grille de taille N x N (ici N=10), une rotation de **90° dans le sens horaire** transforme une coordonnée (ligne, colonne) selon la formule :

(r, c) → (c, N - 1 - r)

À chaque rotation, de nouvelles lettres sont révélées. Pour que le message soit complet, on effectue **4 rotations** (0°, 90°, 180°, 270°).

> **Note importante :** Après chaque rotation, il est impératif de trier les nouvelles positions des trous du haut vers le bas, puis de gauche à droite, pour lire le message dans le bon ordre.
> 

### 4. Solution Automatisée (Python)

```Grandma's Beautiful Scarf/grandma.py```

### 5. Résultat

Après exécution, le script révèle que les mots éparpillés sur la grand-mère étaient des leurres. Le véritable message caché par la grille est :

**`CSC{THE_PATTERN_IS_TANGLED}`**
