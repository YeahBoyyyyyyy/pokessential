import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import requests
from io import BytesIO
from simple_functions import get_ability_description, get_poke_sprite, get_pokemon_types

SPRITE_SCALE = 7
MAX_POKEMON_ID = 1010
MAX_RANDOM_TRIES = 5

class WindowManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Pokemon Sprite Viewer")
        self.root.withdraw()
        self.menu_window = None
        self.label = tk.Label(root)
        self.label.pack(padx=10, pady=10)

    def text_entry_window(
        self,
        prompt,
        callback,
        on_cancel=None,
        window_title="Pokemon",
        size="320x140",
        wraplength=None,
    ):
        def on_submit(_event=None):
            user_input = entry.get().strip()
            should_close = callback(user_input)
            if should_close is not False:
                entry_window.destroy()

        def cancel():
            entry_window.destroy()
            if on_cancel:
                on_cancel()

        entry_window = tk.Toplevel(self.root)
        entry_window.title(window_title)
        entry_window.geometry(size)
        entry_window.resizable(False, False)
        entry_window.protocol("WM_DELETE_WINDOW", cancel)
        label = tk.Label(entry_window, text=prompt)
        if wraplength:
            label.config(wraplength=wraplength, justify="center")
        label.pack(pady=10)
        entry = tk.Entry(entry_window)
        entry.pack(pady=5)
        entry.focus_set()
        tk.Button(entry_window, text="Valider", command=on_submit).pack(pady=10)
        tk.Button(entry_window, text="Annuler", command=cancel).pack()
        entry.bind("<Return>", on_submit)
        entry_window.lift()
        entry_window.focus_force()

    def show_quiz_menu(self):
        if self.menu_window and self.menu_window.winfo_exists():
            self.menu_window.deiconify()
            self.menu_window.lift()
            self.menu_window.focus_force()
            return

        self.menu_window = tk.Toplevel(self.root)
        self.menu_window.title("Quiz Pokemon")
        self.menu_window.geometry("360x240")
        self.menu_window.resizable(False, False)
        self.menu_window.protocol("WM_DELETE_WINDOW", self.root.destroy)
        tk.Label(self.menu_window, text="Choisis un type de quiz :").pack(pady=10)
        tk.Button(
            self.menu_window,
            text="Pokemon par types",
            width=30,
            command=self.start_type_quiz,
        ).pack(pady=5)
        tk.Button(
            self.menu_window,
            text="Deviner Pokemon (sprite)",
            width=30,
            command=self.start_sprite_quiz,
        ).pack(pady=5)
        tk.Button(
            self.menu_window,
            text="Deviner talent (description)",
            width=30,
            command=self.start_ability_quiz,
        ).pack(pady=5)
        self.menu_window.lift()
        self.menu_window.focus_force()

    def _hide_menu(self):
        if self.menu_window and self.menu_window.winfo_exists():
            self.menu_window.withdraw()

    def _show_menu(self):
        if self.menu_window and self.menu_window.winfo_exists():
            self.menu_window.deiconify()
            self.menu_window.lift()
            self.menu_window.focus_force()

    def _close_sprite_window(self):
        self.root.withdraw()
        self._show_menu()

    def _get_random_pokemon(self):
        for _ in range(MAX_RANDOM_TRIES):
            poke_id = random.randint(1, MAX_POKEMON_ID)
            try:
                response = requests.get(
                    f"https://pokeapi.co/api/v2/pokemon/{poke_id}", timeout=10
                )
                response.raise_for_status()
                return response.json()
            except requests.RequestException:
                continue
        return None

    def start_type_quiz(self):
        self._hide_menu()
        data = self._get_random_pokemon()
        if not data:
            messagebox.showerror("Erreur", "Impossible de recuperer un Pokemon.")
            self._show_menu()
            return

        types = [entry["type"]["name"] for entry in data.get("types", [])]
        if not types:
            messagebox.showerror("Erreur", "Types indisponibles.")
            self._show_menu()
            return

        types_text = " / ".join(types)
        prompt = f"Donne un Pokemon avec les types :\n{types_text}"

        def on_submit(pokemon_name):
            if not pokemon_name:
                messagebox.showwarning("Nom manquant", "Entre un nom de Pokemon.")
                return False
            try:
                guessed_types = get_pokemon_types(pokemon_name.lower())
            except Exception:
                messagebox.showerror("Erreur", "Pokemon introuvable.")
                return False

            if all(type_name in guessed_types for type_name in types):
                messagebox.showinfo("Bravo", "Bonne reponse !")
            else:
                messagebox.showinfo("Rate", f"Types attendus : {types_text}")
            self._show_menu()
            return True

        self.text_entry_window(
            prompt,
            on_submit,
            on_cancel=self._show_menu,
            window_title="Quiz Types",
            size="360x160",
            wraplength=340,
        )

    def start_sprite_quiz(self):
        self._hide_menu()
        data = self._get_random_pokemon()
        if not data:
            messagebox.showerror("Erreur", "Impossible de recuperer un Pokemon.")
            self._show_menu()
            return

        answer_name = data.get("name")
        if not answer_name:
            messagebox.showerror("Erreur", "Nom du Pokemon indisponible.")
            self._show_menu()
            return

        try:
            self.open_poke_sprite(answer_name)
        except Exception:
            messagebox.showerror("Erreur", "Impossible d'afficher le sprite.")
            self._show_menu()
            return

        def on_submit(pokemon_name):
            if not pokemon_name:
                messagebox.showwarning("Nom manquant", "Entre un nom de Pokemon.")
                return False
            if pokemon_name.lower() == answer_name.lower():
                messagebox.showinfo("Bravo", "Bonne reponse !")
            else:
                messagebox.showinfo("Rate", f"C'etait : {answer_name}")
            self.root.withdraw()
            self._show_menu()
            return True

        self.text_entry_window(
            "Quel est ce Pokemon ?",
            on_submit,
            on_cancel=self._close_sprite_window,
            window_title="Quiz Sprite",
        )

    def start_ability_quiz(self):
        self._hide_menu()
        data = self._get_random_pokemon()
        if not data:
            messagebox.showerror("Erreur", "Impossible de recuperer un Pokemon.")
            self._show_menu()
            return

        abilities = [entry["ability"]["name"] for entry in data.get("abilities", [])]
        if not abilities:
            messagebox.showerror("Erreur", "Talents indisponibles.")
            self._show_menu()
            return

        ability_name = random.choice(abilities)
        translated_name = None
        description = None
        try:
            translated_name, description = get_ability_description(ability_name, language="fr")
        except Exception:
            translated_name, description = None, None

        if not description:
            try:
                translated_name, description = get_ability_description(ability_name, language="en")
            except Exception:
                translated_name, description = None, None

        if not description:
            messagebox.showerror("Erreur", "Description indisponible.")
            self._show_menu()
            return

        prompt = f"Description du talent :\n{description}\n\nQuel est le nom du talent ?"

        def on_submit(guess):
            if not guess:
                messagebox.showwarning("Nom manquant", "Entre un nom de talent.")
                return False
            normalized_guess = guess.strip().lower().replace(" ", "-")
            normalized_answer = ability_name.lower()
            normalized_translation = (translated_name or "").lower()

            if normalized_guess in (normalized_answer, normalized_translation):
                messagebox.showinfo("Bravo", "Bonne reponse !")
            else:
                expected = translated_name or ability_name
                messagebox.showinfo("Rate", f"Reponse : {expected}")
            self._show_menu()
            return True

        self.text_entry_window(
            prompt,
            on_submit,
            on_cancel=self._show_menu,
            window_title="Quiz Talent",
            size="420x260",
            wraplength=380,
        )

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

        self.text_entry_window(
            "Entrez le nom du Pokemon :",
            on_submit,
            on_cancel=self.root.destroy,
        )

window = tk.Tk()
manager = WindowManager(window)
manager.show_quiz_menu()
window.mainloop()
