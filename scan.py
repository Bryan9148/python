import tkinter as tk
from tkinter import scrolledtext
import subprocess

def scan_network():
    result_text.delete(1.0, tk.END)  # Effacer le texte précédent

    # Exécuter la commande pour scanner les appareils sur le réseau
    try:
        output = subprocess.check_output(["arp", "-a"], universal_newlines=True)
        result_text.insert(tk.END, "Appareils sur le réseau :\n" + output + "\n\n")
        
        # Scanner les ports de chaque appareil
        for line in output.split('\n'):
            if 'dynamic' in line:
                ip_address = line.split()[0]
                result_text.insert(tk.END, f"Scanning ports pour l'adresse IP {ip_address}...\n")
                try:
                    port_scan_output = subprocess.check_output(["nmap", "-p-", ip_address], universal_newlines=True)
                    result_text.insert(tk.END, port_scan_output + "\n")
                except subprocess.CalledProcessError as e:
                    result_text.insert(tk.END, f"Erreur lors du scan des ports pour l'adresse IP {ip_address}: {e}\n")
    except subprocess.CalledProcessError as e:
        result_text.insert(tk.END, "Erreur lors du scan du réseau : " + str(e))

def scan_ip():
    ip_address = ip_entry.get()
    result_text.delete(1.0, tk.END)  # Effacer le texte précédent

    try:
        port_scan_output = subprocess.check_output(["nmap", "-p-", ip_address], universal_newlines=True)
        result_text.insert(tk.END, f"Scan des ports pour l'adresse IP {ip_address} :\n\n")
        result_text.insert(tk.END, port_scan_output + "\n")
    except subprocess.CalledProcessError as e:
        result_text.insert(tk.END, f"Erreur lors du scan des ports pour l'adresse IP {ip_address}: {e}\n")
    except Exception as ex:
        result_text.insert(tk.END, f"Une erreur s'est produite : {ex}\n")

# Créer la fenêtre principale
root = tk.Tk()
root.title("Scanner les appareils et les ports sur le réseau")

# Champ de texte pour saisir l'adresse IP cible
ip_label = tk.Label(root, text="IP cible :")
ip_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)

ip_entry = tk.Entry(root, width=15)
ip_entry.grid(row=0, column=1, padx=10, pady=10)

# Bouton pour lancer le scan avec Nmap
scan_button = tk.Button(root, text="Scan IP", command=scan_ip)
scan_button.grid(row=0, column=2, padx=10, pady=10)

# Bouton pour lancer le scan du réseau
scan_network_button = tk.Button(root, text="Scan du réseau", command=scan_network)
scan_network_button.grid(row=0, column=3, padx=10, pady=10)

# Créer une zone de texte déroulante pour afficher les résultats
result_text = scrolledtext.ScrolledText(root, width=80, height=20)
result_text.grid(row=1, column=0, columnspan=4, padx=10, pady=5, sticky=tk.NSEW)

# Exécuter la boucle principale de l'interface graphique
root.mainloop()
