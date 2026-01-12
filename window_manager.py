import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
from simple_functions import get_poke_sprite

SPRITE_SCALE = 7

class WindowManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Pokemon Sprite Viewer")
        self.root.withdraw()
        self.label = tk.Label(root)
        self.label.pack(padx=10, pady=10)

    def text_entry_window(self, prompt, callback):
        def on_submit(_event=None):
            user_input = entry.get().strip()
            should_close = callback(user_input)
            if should_close is not False:
                entry_window.destroy()

        entry_window = tk.Toplevel(self.root)
        entry_window.title("Pokemon")
        entry_window.geometry("320x140")
        entry_window.resizable(False, False)
        entry_window.protocol("WM_DELETE_WINDOW", self.root.destroy)
        tk.Label(entry_window, text=prompt).pack(pady=10)
        entry = tk.Entry(entry_window)
        entry.pack(pady=5)
        entry.focus_set()
        tk.Button(entry_window, text="Valider", command=on_submit).pack(pady=10)
        tk.Button(entry_window, text="Annuler", command=self.root.destroy).pack()
        entry.bind("<Return>", on_submit)
        entry_window.lift()
        entry_window.focus_force()

    def open_poke_sprite(
        self,
        pokemon_name,
        generation=None,
        game_version=None,
        shiny=False,
        female=False,
        showdown_sprite=False,
        home_sprite=False,
        official_artwork=False,
    ):
        
        sprite_url = get_poke_sprite(
            pokemon_name,
            generation,
            game_version,
            shiny,
            female,
            showdown_sprite,
            home_sprite,
            official_artwork,
        )
        

        
        response = requests.get(sprite_url, timeout=10)
        response.raise_for_status()
        

        img = Image.open(BytesIO(response.content))
        img = img.resize((img.width * SPRITE_SCALE, img.height * SPRITE_SCALE), Image.NEAREST)
        photo = ImageTk.PhotoImage(img)
        self.label.config(image=photo, text="")
        self.label.image = photo
        self.root.deiconify()
        self.root.update_idletasks()
        window_width = photo.width() + 20
        window_height = min(photo.height() + 20, 720)
        self.root.geometry(f"{window_width}x{window_height}")

    def prompt_for_pokemon(self):
        def on_submit(pokemon_name):
            if not pokemon_name:
                messagebox.showwarning("Nom manquant", "Entrez le nom d'un Pokemon.")
                return False
            self.open_poke_sprite(pokemon_name.lower())
            return True

        self.text_entry_window("Entrez le nom du Pokemon :", on_submit)

window = tk.Tk()
manager = WindowManager(window)
manager.prompt_for_pokemon()
window.mainloop()
