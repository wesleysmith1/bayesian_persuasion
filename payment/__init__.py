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
    pass


# PAGES
class Payment(Page):

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            participation_fee=player.session.config['participation_fee']
        )


page_sequence = [Payment,]
