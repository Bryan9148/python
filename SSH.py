import subprocess

def ssh_connect(host, port, username):
    try:
        command = ["ssh", f"{username}@{host}", "-p", str(port)]
        print(f"Connexion à {host}...")

        subprocess.run(command)
    except Exception as e:
        print(f"Erreur lors de la connexion SSH: {e}")

if __name__ == "__main__":
    host = input("Adresse IP/Host: ")
    port = int(input("Port (par défaut 22): ") or 22)
    username = input("Utilisateur: ")

    ssh_connect(host, port, username)
