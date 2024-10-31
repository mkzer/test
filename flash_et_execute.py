import os
import subprocess
import time

def flash_arduino():
    """Flasher le code Arduino sur la carte."""
    try:
        # Construire le chemin relatif vers le fichier .ino
        ino_file_path = os.path.join("test_finale.ino")

        # Construire la commande arduino-cli avec le chemin relatif du fichier .ino
        arduino_cli_command = [
            "arduino-cli",  # Chemin relatif vers l'exécutable arduino-cli (à adapter si nécessaire)
            "upload",
            "-p",
            "COM8",  # Remplacer par le port série approprié si nécessaire
            "--fqbn",
            "arduino:avr:mega",  # Remplacer par le FQBN approprié si nécessaire
            ino_file_path,
        ]
        result = subprocess.run(
            arduino_cli_command,
            check=True,
            text=True,
            capture_output=True,
        )
        print(result.stdout)
        print("Téléversement réussi !")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors du téléversement : {e}")

def run_python_script():
    """Exécuter le script Python."""
    try:
        # Utiliser un chemin relatif pour le script Python
        python_file_path = os.path.join("test_finale_py.py")
        result = subprocess.run(
            ["python", python_file_path],
            check=True,
            text=True,
            capture_output=True,
        )
        print(result.stdout)
        print("Script Python exécuté avec succès !")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution du script Python : {e}")

def flash_and_execute():
    """Fonction principale pour flasher le code Arduino et exécuter le script Python."""
    flash_arduino()
    time.sleep(2)  # Attendre que la carte Arduino se réinitialise
    run_python_script()

if __name__ == "__main__":
    flash_and_execute()