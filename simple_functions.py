import requests
from PIL import Image

GENERATION_DICT = {
    "1": "generation-i",
    "2": "generation-ii",
    "3": "generation-iii",
    "4": "generation-iv",
    "5": "generation-v",
    "6": "generation-vi",
    "7": "generation-vii",
    "8": "generation-viii",
    "9": "generation-ix",
}

def open_poke_sprite(pokemon_name, generation=None, game_version=None, shiny=False, female=False):
    """
    Affiche le sprite d'un Pokémon avec différentes options.
    
    Args:
        pokemon_name: Nom du Pokémon
        generation: Génération (1-9) ou None pour le sprite par défaut
        game_version: Version spécifique du jeu (ex: "red-blue", "gold", "ruby-sapphire", etc.)
        shiny: True pour la version shiny
        female: True pour la version femelle (si disponible)
    """
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
    response = requests.get(url)
    poke = response.json()
    
    # Déterminer quel sprite utiliser
    sprite_url = None
    
    if generation and str(generation) in GENERATION_DICT:
        # Sprite d'une génération spécifique
        gen_key = GENERATION_DICT[str(generation)]
        versions = poke["sprites"]["versions"].get(gen_key, {})
        
        if game_version and game_version in versions:
            # Version de jeu spécifique
            game_sprites = versions[game_version]
        elif versions:
            # Prendre la première version disponible de la génération
            game_sprites = list(versions.values())[0]
        else:
            print(f"Génération {generation} non disponible pour {pokemon_name}")
            game_sprites = {}
        
        # Construire le nom du sprite selon les options
        if isinstance(game_sprites, dict) and 'animated' in game_sprites:
            game_sprites = game_sprites['animated']
        
        if shiny and female:
            sprite_url = game_sprites.get("front_shiny_female")
        elif shiny:
            sprite_url = game_sprites.get("front_shiny")
        elif female:
            sprite_url = game_sprites.get("front_female")
        else:
            sprite_url = game_sprites.get("front_default")
    else:
        # Sprite par défaut (le plus récent)
        if shiny and female:
            sprite_url = poke["sprites"].get("front_shiny_female")
        elif shiny:
            sprite_url = poke["sprites"].get("front_shiny")
        elif female:
            sprite_url = poke["sprites"].get("front_female")
        else:
            sprite_url = poke["sprites"].get("front_default")
    
    if sprite_url:
        response = requests.get(sprite_url, stream=True)
        img = Image.open(response.raw)
        img.show()
        print(f"Sprite affiché: {sprite_url}")
    else:
        print(f"Sprite non disponible pour les options demandées (shiny={shiny}, female={female}, generation={generation})")

def import_all_learned_moves(pokemon_name, generation=None):
    """
    Importe et retourne toutes les attaques apprises par un Pokémon. 
    Prendre la dernière génération où le pokémon est si generation no précisée.
    
    Args:
        pokemon_name: Nom du Pokémon
        generation: Génération spécifique (1-9) ou None pour la dernière génération et on cherche la dernière
    
    Returns:
        Liste des noms des attaques apprises
    """
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
    response = requests.get(url)
    poke = response.json()

    learned_moves = [move["move"]["name"] for move in poke["moves"]]
    return learned_moves

def get_last_pokemon_generation(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
    response = requests.get(url)
    poke = response.json()

    if generation is None:
        for i in range(9, 1, -1):
            gen_key = GENERATION_DICT[str(i)]
            if poke["versions"][gen_key]:
                generation = i
                break
    return generation

def get_pokemon_types(pokemon_name):
    """
    Retourne les types d'un Pokémon donné.
    
    Args:
        pokemon_name: Nom du Pokémon
    
    Returns:
        Liste des types du Pokémon
    """
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
    response = requests.get(url)
    poke = response.json()
    
    types = [t["type"]["name"] for t in poke["types"]]
    return types


if __name__ == "__main__":
    # Exemples d'utilisation:
    open_poke_sprite("bulbasaur", generation=9)
    moves = import_all_learned_moves("bulbasaur", generation=9)
    
    print(moves)
    pass