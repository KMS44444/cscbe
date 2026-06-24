def solve_grandma_scarf():
    # Le motif 10x10 fourni
    pattern_raw = [
        "C S C { G S A N D _",
        "A N L O V E S P N O",
        "_ C G A T } C { C {",
        "G R A N D T A _ L O",
        "L E S T T O _ K N I",
        "T } C S C { I R A T",
        "D M H _ E O V E S _",
        "T O S K N I D E _ S",
        "C R } R A N D M E _",
        "L O V E T _ T O _ A"
    ]
    # Nettoyage de la grille
    grid = [line.replace(" ", "") for line in pattern_raw]
    N = 10

    # Parsing des instructions de tricot (K=Knit/Trou, P=Purl/Saut)
    instructions = [
        ("K", 1), ("P", 4), ("K", 1), ("P", 15), ("K", 1), ("P", 5), 
        ("K", 1), ("P", 15), ("K", 1), ("P", 18), ("K", 1), ("P", 25), ("K", 1)
    ]

    current_pos = 0
    holes = []
    for action, val in instructions:
        if action == "K":
            for _ in range(val):
                holes.append((current_pos // N, current_pos % N))
                current_pos += 1
        else:
            current_pos += val

    # Extraction sur 4 rotations
    flag_chars = []
    for _ in range(4):
        holes.sort() # Lecture de gauche à droite, haut en bas
        for r, c in holes:
            flag_chars.append(grid[r][c])
        
        # Application de la rotation 90° horaire
        holes = [(c, (N - 1) - r) for r, c in holes]

    # Résultat final
    flag = "".join(flag_chars)
    print(f"Flag : {flag[:flag.find('}')+1]}")

solve_grandma_scarf()
