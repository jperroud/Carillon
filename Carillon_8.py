# 
# Dernière modification : 08-11-2024 - JPP

import os
import random
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk
import mido
from mido import MidiFile, MidiTrack, Message
import pygame

# Initialisation de pygame pour jouer le fichier MIDI
pygame.init()
pygame.mixer.init()

# Dictionnaire pour convertir les noms de notes en valeurs MIDI
note_to_midi = {
    'do': 60, 'do#': 61, 'ré': 62, 'ré#': 63, 'mi': 64, 'fa': 65, 'fa#': 66, 'sol': 67, 'sol#': 68, 'la': 69, 'la#': 70, 'si': 71,
    'do1': 72
}

# Fonction de permutation Plain-Bob
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

# Fonction pour créer le fichier MIDI
def create_midi_file(notes_sequences, filename='output.mid'):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    # Utilisation de l'instrument "Tubular Bells" (numéro de programme 14)
    track.append(Message('program_change', program=14, time=0))

    duration = 480

    for sequence in notes_sequences:
        for note in sequence:
            track.append(Message('note_on', note=note, velocity=64, time=0))
            track.append(Message('note_off', note=note, velocity=64, time=duration))

    try:
        mid.save(filename)
        if os.path.exists(filename):
            print(f"Fichier MIDI créé avec succès : {os.path.abspath(filename)}")
            messagebox.showinfo("Succès", f"Fichier MIDI créé avec succès : {os.path.abspath(filename)}")
        else:
            print(f"Erreur : Le fichier MIDI n'a pas pu être créé à l'emplacement {os.path.abspath(filename)}")
            messagebox.showerror("Erreur", f"Le fichier MIDI n'a pas pu être créé à l'emplacement {os.path.abspath(filename)}")
    except Exception as e:
        print(f"Une erreur s'est produite lors de la sauvegarde du fichier MIDI : {e}")
        messagebox.showerror("Erreur", f"Une erreur s'est produite lors de la sauvegarde du fichier MIDI : {e}")

# Fonction pour jouer le fichier MIDI
def play_midi_file(filename='output.mid'):
    try:
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        messagebox.showinfo("Lecture", "Lecture du fichier MIDI en cours.")
    except Exception as e:
        print(f"Une erreur s'est produite lors de la lecture du fichier MIDI : {e}")
        messagebox.showerror("Erreur", f"Une erreur s'est produite lors de la lecture du fichier MIDI : {e}")

# Fonction pour générer des notes aléatoires
def generate_random_notes(num_bells):
    notes = random.choices(list(note_to_midi.values()), k=num_bells)
    return notes

# Interface graphique
class CarillonApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Carillon")
        self.geometry("600x400")

        self.num_bells = tk.IntVar(value=3)
        self.notes = []

        self.create_widgets()

    def create_widgets(self):
        # Nombre de cloches
        tk.Label(self, text="Nombre de cloches (3-10) :").pack(pady=5)
        tk.Spinbox(self, from_=3, to=10, textvariable=self.num_bells, command=self.update_notes_entry).pack(pady=5)

        # Notes des cloches
        self.notes_frame = tk.Frame(self)
        self.notes_frame.pack(pady=10)
        self.update_notes_entry()

        # Boutons
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(pady=20)

        tk.Button(self.button_frame, text="Générer des notes aléatoires", command=self.generate_random_notes).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="Écouter le carillon", command=self.play_carillon).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="Exporter en fichier MIDI", command=self.export_midi).pack(side=tk.LEFT, padx=5)

    def update_notes_entry(self):
        for widget in self.notes_frame.winfo_children():
            widget.destroy()

        self.notes_entries = []
        for i in range(self.num_bells.get()):
            entry = tk.Entry(self.notes_frame)
            entry.pack(pady=2)
            self.notes_entries.append(entry)

    def generate_random_notes(self):
        self.notes = generate_random_notes(self.num_bells.get())
        for i, entry in enumerate(self.notes_entries):
            note_name = list(note_to_midi.keys())[list(note_to_midi.values()).index(self.notes[i])]
            entry.delete(0, tk.END)
            entry.insert(0, note_name)

    def play_carillon(self):
        self.collect_notes()
        if self.notes:
            permuted_sequences = plain_bob_permutation(self.notes)
            script_name = os.path.splitext(os.path.basename(__file__))[0]
            output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{script_name}.mid")
            create_midi_file(permuted_sequences, filename=output_path)
            play_midi_file(filename=output_path)

    def export_midi(self):
        self.collect_notes()
        if self.notes:
            permuted_sequences = plain_bob_permutation(self.notes)
            script_name = os.path.splitext(os.path.basename(__file__))[0]
            default_filename = f"{script_name}.mid"
            filename = simpledialog.askstring("Nom du fichier", "Entrez le nom du fichier MIDI :", initialvalue=default_filename)
            if filename:
                if not filename.endswith('.mid'):
                    filename += '.mid'
                output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
                create_midi_file(permuted_sequences, filename=output_path)

    def collect_notes(self):
        self.notes = []
        for entry in self.notes_entries:
            note_name = entry.get().lower()
            if note_name in note_to_midi:
                self.notes.append(note_to_midi[note_name])
            else:
                messagebox.showerror("Erreur", f"Note invalide : {note_name}")
                self.notes = []
                break

if __name__ == "__main__":
    app = CarillonApp()
    app.mainloop()
