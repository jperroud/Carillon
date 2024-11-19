import mido
from mido import MidiFile, MidiTrack, Message

def plain_bob_permutation(notes):
    # Applique l'algorithme de permutation "Plain-Bob" à une liste de notes
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
    # Crée un fichier MIDI avec les notes données
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    # Ajouter un message de tempo (optionnel)
    track.append(Message('program_change', program=12, time=0))

    # Durée de chaque note en ticks
    duration = 480

    for note in notes:
        track.append(Message('note_on', note=note, velocity=64, time=0))
        track.append(Message('note_off', note=note, velocity=64, time=duration))

    mid.save(filename)

# Notes de musique en format MIDI (exemple : Do, Ré, Mi, Fa, Sol)
input_notes = [60, 62, 64, 65, 67]  # C4, D4, E4, F4, G4

# Appliquer l'algorithme de permutation "Plain-Bob"
permuted_notes = plain_bob_permutation(input_notes)

# Créer le fichier MIDI avec les notes permutées
create_midi_file(permuted_notes)

print(f"Fichier MIDI créé avec les notes permutées : {permuted_notes}")
