import os
import sys
import mido
from mido import MidiFile, MidiTrack, Message

# Obtenir le répertoire du script Python
script_dir = os.path.dirname(os.path.abspath(__file__))
print("Répertoire du script :", script_dir)
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

# Notes de musique en format MIDI (exemple : Do, Ré, Mi, Fa, Sol)
input_notes = [60, 62, 64, 65, 67]  # C4, D4, E4, F4, G4

# Appliquer l'algorithme de permutation "Plain-Bob"
permuted_notes = plain_bob_permutation(input_notes)

print(f"Notes permutées : {permuted_notes}")

# Créer le fichier MIDI avec les notes permutées
output_filename = 'output.mid'
output_path_script_dir = os.path.join(script_dir, output_filename)
output_path_current_dir = os.path.join(os.getcwd(), output_filename)

try:
    create_midi_file(permuted_notes, filename=output_path_script_dir)
except Exception as e:
    print(f"Une erreur s'est produite lors de la création du fichier MIDI dans le répertoire du script : {e}")
    try:
        create_midi_file(permuted_notes, filename=output_path_current_dir)
    except Exception as e:
        print(f"Une erreur s'est produite lors de la création du fichier MIDI dans le répertoire courant : {e}")

# Vérifier si le fichier a été créé
if os.path.exists(output_path_script_dir):
    print(f"Fichier MIDI trouvé dans le répertoire du script : {output_path_script_dir}")
elif os.path.exists(output_path_current_dir):
    print(f"Fichier MIDI trouvé dans le répertoire courant : {output_path_current_dir}")
else:
    print("Fichier MIDI non trouvé. Vérifiez les permissions d'écriture et les chemins d'accès.")

print("Fin du programme")
