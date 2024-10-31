import tkinter as tk
import serial
import time

# Configuration du port série
ser = serial.Serial('COM8', 9600)  # Assurez-vous que le port COM est correct
time.sleep(2)

# Paramètres de la grille
ROWS = 16
COLS = 24
CELL_SIZE = 20

# Création de la fenêtre Tkinter
root = tk.Tk()
root.title("Automate Cellulaire - Simulation")

# Grille d'états (1 pour vivant, 0 pour mort)
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

# Ouvrir un fichier pour enregistrer les états
log_file = open("automate_simulation.log", "w")

# Fonction pour basculer l'état d'une cellule
def toggle_cell(row, col):
    if grid[row][col] == 0:
        grid[row][col] = 1
        canvas.itemconfig(cell_buttons[row][col], fill="red")
    else:
        grid[row][col] = 0
        canvas.itemconfig(cell_buttons[row][col], fill="white")

# Créer un canevas pour dessiner la grille
canvas = tk.Canvas(root, width=COLS * CELL_SIZE, height=ROWS * CELL_SIZE)
canvas.pack()

# Créer une grille de rectangles
cell_buttons = []
for i in range(ROWS):
    row_buttons = []
    for j in range(COLS):
        rect = canvas.create_rectangle(j * CELL_SIZE, i * CELL_SIZE,
                                       (j + 1) * CELL_SIZE, (i + 1) * CELL_SIZE,
                                       fill="white")
        row_buttons.append(rect)
        canvas.tag_bind(rect, '<Button-1>', lambda event, row=i, col=j: toggle_cell(row, col))
    cell_buttons.append(row_buttons)

# Fonction pour envoyer la grille d'états à l'Arduino
def send_initial_state():
    for row in grid:
        line = ''.join(map(str, row))
        ser.write(line.encode() + b'\n')  # Assurez-vous d'envoyer un caractère de nouvelle ligne
    time.sleep(0.1)

# Fonction pour démarrer la simulation avec Fredkin 1
def start_fredkin1():
    ser.write(b'start1\n')
    receive_statistics()

# Fonction pour démarrer la simulation avec Fredkin 2
def start_fredkin2():
    ser.write(b'start2\n')
    receive_statistics()

# Fonction pour recevoir et enregistrer les statistiques
def receive_statistics():
    while ser.in_waiting > 0:
        line = ser.readline().decode().strip()
        if line.isdigit():
            # Enregistrer dans le fichier log
            log_file.write(f"Génération {line} :\n")
            print(f"Génération {line} enregistrée")
        else:
            # Écrire l'état de la grille dans le fichier
            log_file.write(line + '\n')
    root.after(100, receive_statistics)

# Bouton pour envoyer l'état initial
send_button = tk.Button(root, text="Envoyer l'état initial", command=send_initial_state)
send_button.pack()

# Boutons pour choisir entre Fredkin 1 et Fredkin 2
start_button1 = tk.Button(root, text="Commencer Fredkin 1", command=start_fredkin1)
start_button1.pack()

start_button2 = tk.Button(root, text="Commencer Fredkin 2", command=start_fredkin2)
start_button2.pack()

# Label pour afficher le numéro de génération
generation_label = tk.Label(root, text="Génération: 0")
generation_label.pack()

# Lancer la boucle Tkinter
root.mainloop()

# Fermer le fichier et le port série après la fermeture
log_file.close()
ser.close()