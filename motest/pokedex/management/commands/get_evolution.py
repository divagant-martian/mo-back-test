from django.core.management.base import BaseCommand, CommandError
from pokedex.models import Pokemon
from pokedex.management.commands._logic import getEvolutionChain


class Command(BaseCommand):
    help = """Gets the evolution chain by id from pokeapi.co.

    Pokemons that are new to the database get added.
    Evolutions new to the database get added.
    """

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('evolution_chain_id', type=int)

    def handle(self, *args, **options):
        # Naively assume everything works always
        (pokemon_list,
         links) = getEvolutionChain(options["evolution_chain_id"])
        for info in pokemon_list:
            self.stdout.write("saving pokemon {}".format(info))
            p = Pokemon(**info)
            p.save()
        for (p_from, p_to) in links:
            self.stdout.write("saving link ({}, {})".format(p_from, p_to))
            evolution = Pokemon.objects.filter(id=p_to)[0]
            pre_evolution = Pokemon.objects.filter(id=p_from)[0]
            evolution.pre_evolution = pre_evolution
            evolution.save()
