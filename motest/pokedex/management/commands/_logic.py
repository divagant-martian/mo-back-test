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

    # get the URL for the default Pokemon. Defaults to the first one
    pokemon_url = varieties[0]["pokemon"]["url"]
    for variety in varieties:
        if variety["is_default"]:
            pokemon_url = variety["pokemon"]["url"]

    # get the information of the Pokemon.
    pokemon_info = getResponse(pokemon_url)

    # filter the attributes that we care about
    pokemon = {k: pokemon_info[k] for k in ["id", "name", "weight", "height"]}

    # reorganize the stats to just be the name and value of each stat
    for stat in pokemon_info["stats"]:
        stat_name = stat["stat"]["name"].replace("-", "_")
        pokemon[stat_name] = stat["base_stat"]

    return pokemon


def getEvolutionChain(chain_id):
    """
    Return a evolution chain as a graph of the default Pokemon of each species.

    Args:
        chain_id: ID for the evolution chain

    Returns:
        Graph for the evolution chain as a tuple (V, E), where V contains all
        pokemon present in the graph, and E contains all pairs (p1, p2) such
        that p1 evolves to p2. V is a list of dicts, E is a list of (id1, id2)
    """
    url = evolutionChainUrl(chain_id)
    chain = getResponse(url)["chain"]

    species_nodes = set()  # known pokemons species
    species_links = []  # known links

    # traverse the evolution chain. Each element of the stack is a tuple with
    # the species URL and the list of species it evolves to.
    stack = []

    # start from the root of the chain
    species_url = chain["species"]["url"]
    evolutions = chain["evolves_to"]
    stack.append((species_url, evolutions))

    while len(stack) > 0:
        # take an element from the top of the stack
        (species_url, evolutions) = stack.pop()
        species_nodes.add(species_url)

        for evolution in evolutions:
            evolved_species_url = evolution["species"]["url"]
            # add to the links the current species and the evolved species URL
            species_links.append((species_url, evolved_species_url))
            # add the evolved species URL and its evolutions to the stack
            stack.append((evolved_species_url, evolution["evolves_to"]))
    # NOTE this process does not need to check for visited nodes since there are
    # no cycles in the graph

    # transform this graph of species into a graph of Pokemon

    # get the information of each Pokemon indexed by its species URL
    poke_nodes = {
        species_url: getPokemon(species_url)
        for species_url in species_nodes
    }

    # here we store the evolution links between two Pokemon using their IDs
    poke_links = [(poke_nodes[species_from]["id"],
                   poke_nodes[species_to]["id"])
                  for (species_from, species_to) in species_links]

    # reindex the Pokemon by their own IDs instead of their species URL
    poke_nodes = [poke for poke in poke_nodes.values()]

    return (poke_nodes, poke_links)
