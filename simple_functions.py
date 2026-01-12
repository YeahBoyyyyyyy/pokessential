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

def get_ability_name_translation(ability_name, target_language="fr"):
    """
    Retourne la traduction du nom d'une capacité dans la langue spécifiée.
    
    Args:
        ability_name: Nom du talent en anglais
        target_language: Code de la langue cible (ex: "fr", "es", etc.)
    
    Returns:
        Nom traduit du talent
    """
    url = f"https://pokeapi.co/api/v2/ability/{ability_name}"
    response = requests.get(url)
    ability_data = response.json()
    
    translated_name = None
    for entry in ability_data["names"]:
        if entry["language"]["name"] == target_language:
            translated_name = entry["name"]
            break
    
    return translated_name

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

    for entry in ability_data["flavor_text_entries"][::-1]: # On prend la dernière entrée pour avoir la description la plus récente
        print(entry)
        if entry["language"]["name"] == language:
            desc = entry["flavor_text"].replace("\n", " ").replace("\f", " ")
            break
    
    name = get_ability_name_translation(ability_name, target_language=language)

    return name, desc

def get_pokemon_name_translation(pokemon_name, target_language="fr"):
    """
    Retourne la traduction du nom d'un Pokémon dans la langue spécifiée.
    
    Args:
        pokemon_name: Nom du Pokémon en anglais
        target_language: Code de la langue cible (ex: "fr", "es", etc.)
    
    Returns:
        Nom traduit du Pokémon
    """
    url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_name}"
    response = requests.get(url)
    species_data = response.json()
    
    translated_name = None
    for entry in species_data["names"]:
        if entry["language"]["name"] == target_language:
            translated_name = entry["name"]
            break
    
    return translated_name

def download_pokemon_cry(pokemon_name):
    """
    Télécharge le cri d'un Pokémon depuis PokéAPI.
    
    Args:
        pokemon_name: Nom du Pokémon
    
    Returns:
        URL du fichier audio du cri
    """
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
    response = requests.get(url)
    poke = response.json()
    
    cry_url = poke["cries"].get("latest")
    return cry_url

def get_pokemon_base_stats(pokemon_name):
    """
    Retourne les statistiques de base d'un Pokémon.
    
    Args:
        pokemon_name: Nom du Pokémon
    
    Returns:
        Dictionnaire des statistiques de base
    """
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
    response = requests.get(url)
    poke = response.json()
    
    base_stats = {stat["stat"]["name"]: stat["base_stat"] for stat in poke["stats"]}
    return base_stats

def get_pokemon_height_weight(pokemon_name):
    """
    Retourne la taille et le poids d'un Pokémon.
    
    Args:
        pokemon_name: Nom du Pokémon
    
    Returns:
        Tuple (taille en décimètres, poids en hectogrammes)
    """
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
    response = requests.get(url)
    poke = response.json()
    
    height = poke["height"]
    weight = poke["weight"]
    return height, weight

def get_pokemon_abilities(pokemon_name):
    """
    Retourne les capacités d'un Pokémon.
    
    Args:
        pokemon_name: Nom du Pokémon
    
    Returns:
        Liste des noms des capacités
    """
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
    response = requests.get(url)
    poke = response.json()
    
    abilities = [ability["ability"]["name"] for ability in poke["abilities"]]
    return abilities

def get_pokeball_list():
    """
    Retourne la liste des Pokéballs disponibles dans PokéAPI.
    
    Returns:
        Liste des noms des Pokéballs
    """
    url1 = "https://pokeapi.co/api/v2/item-category/33/"
    url2 = "https://pokeapi.co/api/v2/item-category/34/"
    url3 = "https://pokeapi.co/api/v2/item-category/39/"
    response1 = requests.get(url1)
    response2 = requests.get(url2)
    response3 = requests.get(url3)
    category_data1 = response1.json()
    category_data2 = response2.json()
    category_data3 = response3.json()
    pokeballs = [item["name"] for item in category_data1["items"]]
    pokeballs += [item["name"] for item in category_data2["items"]]
    pokeballs += [item["name"] for item in category_data3["items"]]
    return pokeballs

def get_pokeball_sprite(pokeball_name):
    """
    Retourne l'URL du sprite d'une Pokéball.
    
    Args:
        pokeball_name: Nom de la Pokéball
    
    Returns:
        URL du sprite de la Pokéball
    """
    url = f"https://pokeapi.co/api/v2/item/{pokeball_name}"
    response = requests.get(url)
    item_data = response.json()
    
    sprite_url = item_data["sprites"]["default"]
    return sprite_url

if __name__ == "__main__":
    # Exemples d'utilisation:
    print(get_pokeball_list())
    print(get_pokeball_sprite("poke-ball"))
    pass