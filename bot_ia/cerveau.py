import random

from bot_ia import const
from bot_ia import plateau
from bot_ia import case
from bot_ia import joueur

def get_cases_color(le_plateau: dict[str, dict], pos: tuple[int], direction: str, dist_max: int) -> list[str]:
    """Donne la liste de chaque couleur de chaque case d'une direction.

    Args:
        le_plateau (dict[str, dict]): La matrice qui correspond au plateau de jeu.
        pos (tuple[int]): Position actuel du joueur.
        direction (str): La direction à analyser.
        dist_max (int): La distance limit à analyser.

    Returns:
        list[str]: Liste des couleur dans l'ordre de chaque case
    """    
    rep = []
    nb_lignes = plateau.get_nb_lignes(le_plateau)
    nb_colonnes = plateau.get_nb_colonnes(le_plateau)
    for i in range(1, dist_max):
        if direction == "N":
            np_pos = (pos[0] - i, pos[1])
        elif direction == "S":
            np_pos = (pos[0] + i, pos[1])
        elif direction == "O":
            np_pos = (pos[0], pos[1] - i)
        elif direction == "E":
            np_pos = (pos[0], pos[1] + i)
        else:
            break
        # vérifie murs
        if not (0 <= np_pos[0] < nb_lignes and 0 <= np_pos[1] < nb_colonnes):
            break
        la_case = plateau.get_case(le_plateau, np_pos)
        if case.est_mur(la_case):
            break
        rep.append(la_case["couleur"])
    return rep

def get_joueur(le_plateau: dict[str, dict], pos: tuple[int], direction: str, les_joueur: dict[str,dict], distance_max: int) -> list[dict]:
    """Donne la liste des joueur présent dans une direction sous une distance.

    Args:
        le_plateau (dict[str, dict]): La matrice qui correspond au plateau de jeu.
        pos (tuple[int]): Position actuel du joueur.
        direction (str): La direction à analyser.
        les_joueur (dict[str,dict]): Dictionnaire avec les différent joueurs.
        distance_max (int): La distance limit à analyser.

    Returns:
        list[dict]: Liste des joueur
    """    
    rep = []
    nb_lignes = plateau.get_nb_lignes(le_plateau)
    nb_colonnes = plateau.get_nb_colonnes(le_plateau)
    for i in range(1, distance_max):
        if direction == "N":
            np_pos = (pos[0] - i, pos[1])
        elif direction == "S":
            np_pos = (pos[0] + i, pos[1])
        elif direction == "O":
            np_pos = (pos[0], pos[1] - i)
        elif direction == "E":
            np_pos = (pos[0], pos[1] + i)
        else:
            break
        # vérifie murs
        if not (0 <= np_pos[0] < nb_lignes and 0 <= np_pos[1] < nb_colonnes):
            break
        la_case = plateau.get_case(le_plateau, np_pos)
        if case.est_mur(la_case):
            break
        for un_joueur in les_joueur:
            if un_joueur in la_case["joueurs_presents"]:
                rep.append(les_joueur[un_joueur])
    return rep

def dansPlateau(le_plateau: dict[str, dict], pos: tuple[int]) -> bool:
    """Vérifie si la case est dans le plateau

    Args:
        le_plateau (dict[str, dict]): La matrice qui correspond au plateau de jeu.
        pos (tuple[int]): Position actuel du joueur.

    Returns:
        bool: Vérification de la présence sur le plateau de jeu.
    """
    return 0 <= pos[0] < plateau.get_nb_lignes(le_plateau) and 0 <= pos[1] < plateau.get_nb_colonnes(le_plateau)

def bouger(pos: tuple[int], direction: str) -> tuple[int]:
    """Donne la position du déplacement suivent selon une direction.

    Args:
        pos (tuple[int]): Postion actuel du joueur.
        direction (str): La direction choisie.

    Returns:
        tuple[int]: Position suivente
    """    
    if direction == 'N':
        return (pos[0]-1, pos[1])
    if direction == 'S':
        return (pos[0]+1, pos[1])
    if direction == 'O':
        return (pos[0], pos[1]-1)
    if direction == 'E':
        return (pos[0], pos[1]+1)
    return pos

def mes_territoire_voisin(le_plateau: dict[str, dict], pos: tuple[int], deplacement_possible: list[tuple], ma_couleur: str) -> list[str]:
    """Donne les déplacement voisin vers une case de notre couleur.

    Args:
        le_plateau (dict[str, dict]): La matrice qui correspond au plateau de jeu.
        pos (tuple[int]): Postion actuel du joueur.
        deplacement_possible (list[tuple]): Déplacements que l'on peut effectuer.
        ma_couleur (str): Lettre qui correspond à notre couleur.

    Returns:
        list[str]: Liste des directions qui déplace sur notre couleur.
    """    
    moves = []
    for d in deplacement_possible:
        np = bouger(pos, d)
        if dansPlateau(le_plateau, np):
            la_case = plateau.get_case(le_plateau, np)
            if la_case["couleur"] == ma_couleur and not case.est_mur(la_case):
                moves.append(d)
    return moves

def vers_couleur(le_plateau: dict[str, dict], pos: tuple[int], couleur_cible: str, distance_scan: int) -> str:
    """Donne la direction qui rapproche de la couleur cible.

    Args:
        le_plateau (dict[str, dict]): La matrice qui correspond au plateau de jeu.
        pos (tuple[int]): Postion actuel du joueur.
        couleur_cible (str): Couleur rechercher.
        distance_scan (int): Distance à scanner.

    Returns:
        str: Direction qui rapproche de la couleur cible.
    """    
    visiter = set(pos)
    q = []
    head = 0
    for d in "NSOE":
        np = bouger(pos, d)
        if dansPlateau(le_plateau, np):
            la_case = plateau.get_case(le_plateau, np)
            if not case.est_mur(la_case):
                visiter.add(np)
                q.append((np, d, 1))
    while head < len(q):
        cur, first_dir, dist = q[head]
        head += 1
        cur_case = plateau.get_case(le_plateau, cur)
        if cur_case["couleur"] == couleur_cible:
            return first_dir
        if dist < distance_scan:
            for d in "NSOE":
                np = bouger(cur, d)
                if dansPlateau(le_plateau, np) and np not in visiter:
                    la_case = plateau.get_case(le_plateau, np)
                    if not case.est_mur(la_case):
                        visiter.add(np)
                        q.append((np, first_dir, dist+1))
    return None

def vers_autre_couleur(le_plateau: dict[str, dict], pos: tuple[int], couleur_cible: str, distance_scan: int) -> str:
    """Donne la direction qui rapproche des autre couleur que celle de la cible.

    Args:
        le_plateau (dict[str, dict]): La matrice qui correspond au plateau de jeu.
        pos (tuple[int]): Postion actuel du joueur.
        couleur_cible (str): Couleur rechercher.
        distance_scan (int): Distance à scanner.

    Returns:
        str: Direction qui rapproche de la couleur cible.
    """    
    visiter = set(pos)
    q = []
    head = 0
    for d in "NSOE":
        np = bouger(pos, d)
        if dansPlateau(le_plateau, np):
            la_case = plateau.get_case(le_plateau, np)
            if not case.est_mur(la_case):
                visiter.add(np)
                q.append((np, d, 1))
    while head < len(q):
        cur, first_dir, dist = q[head]
        head += 1
        cur_case = plateau.get_case(le_plateau, (cur[0], cur[1]))
        if cur_case["couleur"] != couleur_cible:
            return first_dir
        if dist < distance_scan:
            for d in "NSOE":
                np = bouger(cur, d)
                if dansPlateau(le_plateau, np) and np not in visiter:
                    la_case = plateau.get_case(le_plateau, np)
                    if not case.est_mur(la_case):
                        visiter.add(np)
                        q.append((np, first_dir, dist))
    return None

def trouverObjet(le_plateau, pos, distance_objet):
    visiter = set(pos)
    q = []
    head = 0
    for d in "NSOE":
        np = bouger(pos, d)
        if dansPlateau(le_plateau, np):
            la_case = plateau.get_case(le_plateau, np)
            if not case.est_mur(la_case):
                visiter.add(np)
                q.append((np, d, 1))
    while head < len(q):
        cur, first_dir, dist = q[head]
        head += 1
        cur_case = plateau.get_case(le_plateau, cur)
        if case.get_objet(cur_case) != const.AUCUN:
            return first_dir
        if dist < distance_objet:
            for d in "NSOE":
                np = bouger(cur, d)
                if dansPlateau(le_plateau, np) and np not in visiter:
                    la_case = plateau.get_case(le_plateau, np)
                    if not case.est_mur(la_case):
                        visiter.add(np)
                        q.append((np, first_dir, dist+1))
    return None

def score_point(le_plateau, pos, ma_couleur):
    scoreN = 0
    scoreS = 0
    scoreE = 0
    scoreO = 0

    colorN = get_cases_color(le_plateau, pos, "N", const.PORTEE_PEINTURE)
    colorS = get_cases_color(le_plateau, pos, "S", const.PORTEE_PEINTURE)
    colorE = get_cases_color(le_plateau, pos, "E", const.PORTEE_PEINTURE)
    colorO = get_cases_color(le_plateau, pos, "O", const.PORTEE_PEINTURE)

    for couleur in colorN:
        if couleur == " ":
            scoreN += 1
        elif couleur != ma_couleur:
            scoreN += 2
        else:
            scoreN -= 1
    for couleur in colorS:
        if couleur == " ":
            scoreS += 1
        elif couleur != ma_couleur:
            scoreS += 2
        else:
            scoreS -= 1
    for couleur in colorE:
        if couleur == " ":
            scoreE += 1
        elif couleur != ma_couleur:
            scoreE += 2
        else:
            scoreE -= 1
    for couleur in colorO:
        if couleur == " ":
            scoreO += 1
        elif couleur != ma_couleur:
            scoreO += 2
        else:
            scoreO -= 1

    if scoreN == 0 and scoreS == 0 and scoreO == 0 and scoreE == 0:
        return "X"
    res = {"N": scoreN, "S": scoreS, "E": scoreE, "O": scoreO}
    return max(res, key= lambda x: res[x])

def tir(le_plateau, pos, direction_tir, reserve, ma_couleur, les_joueur):
    nb_joueur_all_direction = {d: plateau.nb_joueurs_direction(le_plateau, pos, d, const.PORTEE_PEINTURE)
                                for d in direction_tir}
    plus_joueur = max(nb_joueur_all_direction, key=lambda x: nb_joueur_all_direction[x])
    if reserve > 5:
        if nb_joueur_all_direction[plus_joueur] <= 1:
            return score_point(le_plateau, pos, ma_couleur)
        else:
            for joueur_analys in get_joueur(le_plateau, pos, plus_joueur, les_joueur, const.PORTEE_PEINTURE):
                if type(joueur_analys) == set:
                    for joueur_analys_2 in joueur_analys:
                        if joueur.get_reserve(joueur_analys_2) > -10 and joueur.get_surface(joueur_analys) > 0:
                            return plus_joueur
            return score_point(le_plateau, pos, ma_couleur)
    return "X"

def deplacement(le_plateau, pos, les_joueurs, reserve, surface, position, ma_couleur, distance_objet, distance_scan):
    dirs_poss = plateau.directions_possibles(le_plateau, pos)
    deplacement_possible = ''.join(dirs_poss.keys())

    # Si le joueur porte un objet -> retourner vers la plus proche case de sa couleur
    if joueur.get_objet(les_joueurs[ma_couleur]) != const.AUCUN:

        # Cherche la case la plus proche de la couleur du joueur
        if plateau.get_case(le_plateau, pos)["couleur"] == ma_couleur:
            found_dir = vers_autre_couleur(le_plateau, pos, ma_couleur, distance_scan)
            if found_dir and found_dir in deplacement_possible:
                return found_dir
        else:
            found_dir = vers_couleur(le_plateau, pos, ma_couleur, distance_scan)
            if found_dir and found_dir in deplacement_possible:
                return found_dir

        # fallback: privilégier rester sur la même couleur si possible
        if deplacement_possible == "X":
            return "X"
        same_color = mes_territoire_voisin(le_plateau, pos, deplacement_possible, ma_couleur)
        if same_color:
            return random.choice(same_color)
        return random.choice(deplacement_possible)

    # Si le joueur n'a pas d'objet -> n'avancer hors couleur que si un objet est trouvé dans `distance_max`
    if (reserve < 5 and surface <= 5):
        found_dir = trouverObjet(le_plateau, pos, distance_objet=150)
        if found_dir and found_dir in deplacement_possible:
            return found_dir
    else:
        found_dir = trouverObjet(le_plateau, pos, distance_objet)
        if found_dir and found_dir in deplacement_possible:
            return found_dir

    # Sinon, on se déplace uniquement sur sa couleur si possible
    if plateau.get_case(le_plateau, pos)["couleur"] == ma_couleur and reserve > 5 :
        found_dir = vers_autre_couleur(le_plateau, pos, ma_couleur, distance_scan)
        if found_dir and found_dir in deplacement_possible:
            return found_dir
    else:
        found_dir = vers_couleur(le_plateau, pos, ma_couleur, distance_scan)
        if found_dir and found_dir in deplacement_possible:
            return found_dir
    same_color = mes_territoire_voisin(le_plateau, pos, deplacement_possible, ma_couleur)
    if same_color:
        return random.choice(same_color)
    return random.choice(deplacement_possible)