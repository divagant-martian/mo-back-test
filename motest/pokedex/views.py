from django.http import HttpResponse
from .models import Pokemon
from django.core import serializers
from django.forms.models import model_to_dict
import json

def search(request, name):
    """Searches for a Pokemon with the given name

    Args:
        request: http request (ignores GET/POST)
        name: string to look for

    Returns:
        json HttpResponse including the pokemon related to the query, the
        pokemon from which it evolves, and a list of evolutions
    """
    # clean the name to get more hits
    # TODO fuzzy search or surstring search
    name = name.strip().lower()
    # search the pokemon
    qs = Pokemon.objects.filter(name=name)
    r = {}
    if len(qs) > 0:
        # fields to serialize for the evolutions/preevolutions
        keep = ("id", "name")
        pokemon = qs[0]
        # serialize our pokemon
        pokemon_info = model_to_dict(pokemon, exclude="pre_evolution")
        # get its pre_evolution, if any, and serialize it
        evolves_from = pokemon.pre_evolution
        if evolves_from:
            evolves_from = model_to_dict(pokemon.pre_evolution, fields=keep)
        # get its evolutions and serialize them
        evolves_to = pokemon.evolutions.all()
        evolutions = list(map(lambda e: model_to_dict(e, fields=keep), evolves_to))
        r = {"pokemon": pokemon_info, "evolves_from": evolves_from, "evolves_to":evolutions}
    r = json.dumps(r)
    return HttpResponse(r, content_type='application/json')

# Create your views here.
