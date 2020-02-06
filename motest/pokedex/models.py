from django.db import models


class Pokemon(models.Model):
    """
    A Pokemon with all the basic info

    Attributes:
        name (str): Name of the pokemon
        height (int): Height of the pokemon
        weight (int): Height of the pokemon

        # Stats of the pokemon
        # https://www.pokemon.com/us/play-pokemon/about/video-game-glossary/#basestat
        speed (int)
        special_defense (int)
        special_attack (int)
        defense (int)
        attack (int)
        hp (int)
    """
    name = models.CharField(max_length=200)
    height = models.IntegerField()
    weight = models.IntegerField()
    speed = models.IntegerField()
    special_defense = models.IntegerField()
    special_attack = models.IntegerField()
    defense = models.IntegerField()
    attack = models.IntegerField()
    hp = models.IntegerField()
    pre_evolution = models.ForeignKey('self',
                                      on_delete=models.CASCADE,
                                      related_name='evolutions',
                                      null=True)

    def __str__(self):
        return self.name
