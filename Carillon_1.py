import os
import mido
from mido import MidiFile, MidiTrack, Message

print("Répertoire de travail actuel :", os.getcwd())
# print("Version de mido :", mido.__version__)

def plain_bob_permutation(notes):
    n = len(notes)
    result = []
    for i in range(n):
        if i % 2 == 0:
            result.append(notes[i])
        else:
            if i + 1 < n:
                result.append(notes[i + 1])
            result.append(notes[i - 1])
    return result

def create_midi_file(notes, filename='output.mid'):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    track.append(Message('program_change', program=12, time=0))

    duration = 480

    for note in notes:
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

def find_file(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
    return None

# Notes de musique en format MIDI (exemple : Do, Ré, Mi, Fa, Sol)
input_notes = [60, 62, 64, 65, 67]  # C4, D4, E4, F4, G4

# Appliquer l'algorithme de permutation "Plain-Bob"
permuted_notes = plain_bob_permutation(input_notes)

print(f"Notes permutées : {permuted_notes}")

# Créer le fichier MIDI avec les notes permutées
output_path = os.path.join(os.getcwd(), 'output.mid')

try:
    create_midi_file(permuted_notes, filename=output_path)
except Exception as e:
    print(f"Une erreur s'est produite lors de la création du fichier MIDI : {e}")

# Vérifier si le fichier a été créé
if os.path.exists(output_path):
    print(f"Fichier MIDI trouvé à : {output_path}")
else:
    print("Fichier MIDI non trouvé à l'emplacement attendu. Recherche sur le système...")
    file_path = find_file('output.mid', '/')
    if file_path:
        print(f"Fichier trouvé à : {file_path}")
    else:
        print("Fichier non trouvé sur le système")

print("Fin du programme")
