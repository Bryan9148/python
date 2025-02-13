import sys

def evaluer_force_mot_de_passe(mot_de_passe):
    force = 0
    
    # Vérifier la longueur du mot de passe
    if len(mot_de_passe) >= 8:
        force += 1
    
    # Vérifier la présence de caractères majuscules et minuscules
    if any(char.isupper() for char in mot_de_passe) and any(char.islower() for char in mot_de_passe):
        force += 1
    
    # Vérifier la présence de chiffres
    if any(char.isdigit() for char in mot_de_passe):
        force += 1
    
    # Vérifier la présence de caractères spéciaux
    if any(char in "!@#$%^&*()_+{}[];:<>,.?/" for char in mot_de_passe):
        force += 1
    
    return force

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Utilisation : python script.py <mot_de_passe>")
        sys.exit(1)

    mot_de_passe = sys.argv[1]
    force = evaluer_force_mot_de_passe(mot_de_passe)
    print(f"Force du mot de passe : {force}/4")
