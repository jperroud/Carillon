import os
import mido
from mido import MidiFile, MidiTrack, Message

# Obtenir le répertoire du script Python
script_dir = os.path.dirname(os.path.abspath(__file__))
print("Répertoire du script :", script_dir)
print("Répertoire de travail actuel :", os.getcwd())

# Vérification de la version de mido de manière sûre
try:
    mido_version = mido.__version__
except AttributeError:
    mido_version = "Version inconnue"
print("Version de mido :", mido_version)

# Dictionnaire pour convertir les noms de notes en valeurs MIDI
note_to_midi = {
    'do2': 36, 're2': 38, 'mi2': 40, 'fa2': 41, 'sol2': 43, 'la2': 45, 'si2': 47,
    'do3': 48, 're3': 50, 'mi3': 52, 'fa3': 53, 'sol3': 55, 'la3': 57, 'si3': 59,
    'do4': 60, 're4': 62, 'mi4': 64, 'fa4': 65, 'sol4': 67, 'la4': 69, 'si4': 71
}

def plain_bob_permutation(notes):
    original_notes = notes.copy()
    result = [notes.copy()]
    max_iterations = 120  # Limite pour éviter une boucle infinie
    iterations = 0

    while True:
        new_sequence = notes.copy()
        
        # Permutation Plain-Bob
        if iterations % 2 == 0:
            # Échange des paires adjacentes, sauf la dernière paire
            for i in range(0, len(new_sequence) - 2, 2):
                new_sequence[i], new_sequence[i + 1] = new_sequence[i + 1], new_sequence[i]
        else:
            # Échange des paires adjacentes, en commençant par la deuxième note
            for i in range(1, len(new_sequence) - 1, 2):
                new_sequence[i], new_sequence[i + 1] = new_sequence[i + 1], new_sequence[i]

        notes = new_sequence
        result.append(notes)
        iterations += 1

        if notes == original_notes or iterations >= max_iterations:
            break

    return result

def create_midi_file(notes_sequences, filename='output.mid'):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    track.append(Message('program_change', program=12, time=0))

    duration = 480

    for sequence in notes_sequences:
        for note in sequence:
            track.append(Message('note_on', note=note, velocity=64, time=0))
            track.append(Message('note_off', note=note, velocity=64, time=duration))

    try:
        mid.save(filename)
        if os.path.exists(filename):
            print(f"Fichier MIDI créé avec succès : {os.path.abspath(filename)}")
        else:
            print(f"Erreur : Le fichier MIDI n'a pas pu être créé à l'emplacement {os.path.abspath(filename)}")
    except Exception as e:
        print(f"Une erreur s'est produite lors de la sauvegarde du fichier MIDI : {e}")

# Demander le nombre de cloches
while True:
    try:
        num_bells = int(input("Combien de cloches souhaitez-vous utiliser ? (min 3, max 10) : "))
        if 3 <= num_bells <= 10:
            break
        else:
            print("Veuillez entrer un nombre entre 3 et 10.")
    except ValueError:
        print("Veuillez entrer un nombre valide.")

# Demander les notes pour chaque cloche
input_notes = []
for i in range(num_bells):
    while True:
        note = input(f"Entrez la note pour la cloche {i + 1} (ex: do3, re3, mi3, etc.) : ").lower()
        if note in note_to_midi:
            input_notes.append(note_to_midi[note])
            break
        else:
            print("Note invalide. Veuillez entrer une note valide (ex: do3, re3, mi3, etc.).")

# Appliquer l'algorithme de permutation "Plain-Bob"
permuted_sequences = plain_bob_permutation(input_notes)

print("Séquences de notes permutées :")
for i, seq in enumerate(permuted_sequences):
    print(f"Séquence {i+1}: {seq}")

# Créer le fichier MIDI avec les séquences de notes permutées
output_filename = 'output.mid'
output_path = os.path.join(script_dir, output_filename)

try:
    create_midi_file(permuted_sequences, filename=output_path)
except Exception as e:
    print(f"Une erreur s'est produite lors de la création du fichier MIDI : {e}")

# Vérifier si le fichier a été créé
if os.path.exists(output_path):
    print(f"Fichier MIDI trouvé à : {output_path}")
else:
    print("Fichier MIDI non trouvé. Vérifiez les permissions d'écriture et les chemins d'accès.")

print("Fin du programme")
