from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'payment'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    name = models.StringField()


# PAGES
class Payment1(Page):
    form_model = 'player'
    form_fields = ['name']


class Payment2(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(participation_fee=player.session.config['participation_fee'],)


class Final(Page):
    pass


page_sequence = [Payment1, Payment2, Final]
