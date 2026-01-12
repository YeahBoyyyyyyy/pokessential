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

def search_pokemon_list_from_types(type1, type2=None):
    """
    Recherche des Pokémon par types.
    
    Args:
        type1: Premier type
        type2: Deuxième type (optionnel)
    
    Returns:
        Liste des noms des Pokémon correspondant aux types
    """
    url = f"https://pokeapi.co/api/v2/type/{type1}"
    response = requests.get(url)
    type_data = response.json()
    
    pokemon_list = [p["pokemon"]["name"] for p in type_data["pokemon"]] # type_data["pokemon"] est une liste de dictionnaires
    
    if type2:
        url2 = f"https://pokeapi.co/api/v2/type/{type2}"
        response2 = requests.get(url2)
        type_data2 = response2.json()
        
        pokemon_list_type2 = {p["pokemon"]["name"] for p in type_data2["pokemon"]}
        # Filtrer les Pokémon qui ont les deux types
        pokemon_list = [p for p in pokemon_list if p in pokemon_list_type2]
    
    return pokemon_list

def get_ability_description(ability_name, language="en"):
    """
    Retourne la description d'une capacité dans la langue spécifiée.
    
    Args:
        ability_name: Nom du talent
        language: Code de la langue (ex: "en", "fr", etc.)
    Returns:
        Description du talent
    """
    # Petite correction de ability_name pour les capacités avec des espaces ou des traits d'union
    for i_car in range(len(ability_name)):
        if ability_name[i_car] == " " or ability_name[i_car] == "_":
            ability_name[i_car] = "-"


    url = f"https://pokeapi.co/api/v2/ability/{ability_name}"
    response = requests.get(url)
    ability_data = response.json()
    desc = None
    name = None
    for entry in ability_data["flavor_text_entries"][::-1]: # On prend la dernière entrée pour avoir la description la plus récente
        print(entry)
        if entry["language"]["name"] == language:
            desc = entry["flavor_text"].replace("\n", " ").replace("\f", " ")
            break
    for entry in ability_data["names"]:
        if entry["language"]["name"] == language:
            name = entry["name"]
            break
    return name, desc

if __name__ == "__main__":
    # Exemples d'utilisation:
    list = get_ability_description("drizzle", language="fr")
    print(list)

    pass