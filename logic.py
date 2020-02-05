import requests


def getResponse(url):
    """
    Do a get request and return the body of the response as JSON.

    Args:
        url: URL to do the get request

    Returns:
        A dictionary with the body of the response.

    Raises:
        HTTPError: If the response status code is not OK.
        JSONDecodeError: If the body of the response is not a valid JSON.
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def evolutionChainUrl(chain_id):
    """
    Return an URL for a specific evolution chain.

    Args:
        chain_id: ID for the evolution chain

    Returns:
        URL for the evolution chain

    Raises:
        ValueError: if chain_id is not an integer
    """
    if not isinstance(chain_id, int):
        raise ValueError(
            "Expected integer evolution chain id, found {}".format(chain_id))

    return "https://pokeapi.co/api/v2/evolution-chain/{}".format(chain_id)


def getPokemon(species_url):
    """
    Return the attributes of the default Pokemon of a species.

    If the species does not have a default variety, it returns the first
    Pokemon variety.

    Args:
        species_url: URL of the species

    Returns:
        Dictionary with the default Pokemon attributes

    Raises:
        IndexError: if the species does not have any Pokemon varieties.
    """
    # Get species information from URL
    species = getResponse(species_url)

    varieties = species["varieties"]
    # Raise error if varieties are empty
    if len(varieties) == 0:
        raise IndexError("Species {} has no varieties".format(species["name"]))

    # get the URL for the default Pokemon
    pokemon_url = None
    for variety in varieties:
        if variety["is_default"]:
            pokemon_url = variety["pokemon"]["url"]

    # this can only be None if no variety was the default one
    if pokemon_url is None:
        pokemon_url = varieties[0]["pokemon"]["url"]

    # get the information of the Pokemon.
    pokemon = getResponse(pokemon_url)

    # filter the attributes that we care about
    pokemon = {
        k: pokemon[k]
        for k in ["id", "name", "stats", "weight", "height"]
    }

    # reorganize the stats to just be the name and value of each stat
    pokemon["stats"] = [{
        "name": stat["stat"]["name"],
        "base": stat["base_stat"]
    } for stat in pokemon["stats"]]

    return pokemon


def getEvolutionChain(chain_id):
    """
    Return a evolution chain as a graph of the default Pokemon of each species.

    Args:
        chain_id: ID for the evolution chain

    Returns:
        Graph for the evolution chain as a tuple. The first element is a
        dictionary with the Pokemon indexed by ID and the second element is a
        list with the evolution links between Pokemon IDs

    """
    url = evolutionChainUrl(chain_id)
    # get the evolution chain information from the URL
    chain = getResponse(url)["chain"]

    # build a graph for the species, where each node is a species, and two
    # species are linked if the first species evolves into the second

    species_nodes = set()
    species_links = []

    # traverse the evolution chain using DFS. Each element of the stack is a
    # tuple with the species URL and the species it evolves to.
    stack = []

    # start from the root of the chain
    species_url = chain["species"]["url"]
    evolutions = chain["evolves_to"]
    stack.append((species_url, evolutions))

    while len(stack) > 0:
        # take an element from the top of the stack
        (species_url, evolutions) = stack.pop()
        # add the species URL to the nodes set
        species_nodes.add(species_url)

        for evolution in evolutions:
            # get the URL of the evolved species
            evolved_species_url = evolution["species"]["url"]
            # add to the links the current species and the evolved species URL
            species_links.append((species_url, evolved_species_url))
            # add the evolved species URL and its evolutions to the stack
            stack.append((evolved_species_url, evolution["evolves_to"]))

    # transform this graph of species into a graph of Pokemon

    # get the information of each Pokemon indexed by its species URL
    poke_nodes = {
        species_url: getPokemon(species_url)
        for species_url in species_nodes
    }

    # here we store the evolution links between two Pokemon using their IDs
    poke_links = [{
        "from": poke_nodes[species_from]["id"],
        "to": poke_nodes[species_to]["id"]
    } for (species_from, species_to) in species_links]

    # reindex the Pokemon by their own IDs instead of their species URL
    poke_nodes = {poke["id"]: poke for poke in poke_nodes.values()}

    return (poke_nodes, poke_links)

