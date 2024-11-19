import os
import mido
from mido import MidiFile, MidiTrack, Message

# Obtenir le répertoire du script Python
script_dir = os.path.dirname(os.path.abspath(__file__))
print("Répertoire du script :", script_dir)
print("Répertoire de travail actuel :", os.getcwd())
print("Version de mido :", mido.__version__)

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
        # Suppression de la pause entre les séquences

    try:
        mid.save(filename)
        if os.path.exists(filename):
            print(f"Fichier MIDI créé avec succès : {os.path.abspath(filename)}")
        else:
            print(f"Erreur : Le fichier MIDI n'a pas pu être créé à l'emplacement {os.path.abspath(filename)}")
    except Exception as e:
        print(f"Une erreur s'est produite lors de la sauvegarde du fichier MIDI : {e}")

# Notes de musique en format MIDI (exemple : Do, Ré, Mi, Fa, Sol)
input_notes = [60, 62, 64, 65, 67]  # C4, D4, E4, F4, G4

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
