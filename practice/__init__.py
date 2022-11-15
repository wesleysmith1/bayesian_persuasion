from otree.api import *

import random

doc = """
Your app description
"""

class PostPracticeWait(WaitPage):
    wait_for_all_groups = True
    

class C(BaseConstants):
    NAME_IN_URL = 'practice'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 2

    R = 'Red'
    B = 'Blue'

    PROBABILITY_BLUE = 67
    PROBABILITY_RED = 33

    CHART_TEMPLATE = 'main/chart.html'
    LOADING_TEMPLATE = 'main/loading.html'

    ROUND_PAY = cu(2)

    LOADING_INTERVAL = 3000

    LOADING_STAGES = [
        ["a", "b"],
        ["c", "d"],
        ["e", "f"],
        ["g", "h"]
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    if_red_send_red = models.IntegerField()
    if_red_send_blue = models.IntegerField()
    if_blue_send_red = models.IntegerField()
    if_blue_send_blue = models.IntegerField()

    if_red_guess = models.StringField(choices=[C.R, C.B])
    if_red_flagged_guess = models.StringField(choices=[C.R, C.B])
    if_blue_guess = models.StringField(choices=[C.R, C.B])
    if_blue_flagged_guess = models.StringField(choices=[C.R, C.B])

    ball_color = models.StringField(choices=[C.R, C.B])
    message_sent = models.StringField(choices=[C.R, C.B])
    guess = models.StringField()
    message_flagged = models.BooleanField()

    receiver_payoff = models.CurrencyField(initial=0)
    sender_payoff = models.CurrencyField(initial=0)


class Player(BasePlayer):
    pass


# FUNCTIONS
def creating_session(subsession: Subsession):
    pass


# PAGES
class CommunicationStage(Page):
    form_model = 'group'
    form_fields = ['if_red_send_red', 'if_red_send_blue', 'if_blue_send_red', 'if_blue_send_blue']

    @staticmethod
    def error_message(player, values):
        if values['if_red_send_red'] + values['if_red_send_blue'] != 100:
            return 'The numbers must add up to 100'

        if values['if_blue_send_red'] + values['if_blue_send_blue'] != 100:
            return 'The numbers must add up to 100'


class Wait1(WaitPage):
    pass


class Wait2(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):

        group.ball_color = random.choices([C.R, C.B], [C.PROBABILITY_RED, C.PROBABILITY_BLUE])[0]

        if group.ball_color == C.R:
            group.message_sent = random.choices([C.R, C.B], [group.if_red_send_red, group.if_red_send_blue])[0]
        elif group.ball_color == C.B:
            group.message_sent = random.choices([C.R, C.B], [group.if_blue_send_red, group.if_blue_send_blue])[0]

        # is message false
        if group.ball_color != group.message_sent and group.session.config['flagged'] > 0:
            group.message_flagged = random.random() < group.session.config['flagged']

        if group.ball_color == C.R:
            if group.field_maybe_none('message_flagged'):
                group.guess = group.if_red_flagged_guess
            else:
                group.guess = group.if_red_guess
        else:
            if group.field_maybe_none('message_flagged'):
                group.guess = group.if_blue_flagged_guess
            else:
                group.guess = group.if_blue_guess

        # payoffs
        if group.guess == C.R:
            group.sender_payoff = C.ROUND_PAY

        if group.ball_color == group.guess:
            group.receiver_payoff = C.ROUND_PAY


class GuessingStage(Page):
    form_model = 'group'

    @staticmethod
    def get_form_fields(player):
        if player.session.config["flagged"] > 0:
            return ['if_red_guess', 'if_red_flagged_guess', 'if_blue_guess', 'if_blue_flagged_guess']
        else:
            return ['if_red_guess', 'if_blue_guess']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
                form_elements= 4 if player.session.config["flagged"] > 0 else 2,
                chart_title="The Sender chose this Communication Plan:",
            )


class Summary(Page):
    pass

    @staticmethod
    def vars_for_template(player: Player):
        chart_title = "Sender's Communication Plan"
        return dict(
                form_elements= 4 if player.session.config["flagged"] > 0 else 2,
                chart_title=chart_title,
            )


class LoadingPage(Page):
    @staticmethod
    def vars_for_template(player: Player):

        form_elements= 4 if player.session.config["flagged"] > 0 else 2

        a = [
                "Drawing a ball from bag", 
                "Looking at Sender’s Communication Plan", 
                "Picking message with these probabilities", 
                "Message is going through Flagging Device",
                "Looking at Receiver’s Guessing Plan",
                "Calculating payoffs"
            ]
        
        # remove flagging device with q=0
        if form_elements == 2:
            a.remove("Message is going through Flagging Device")

        b = [
            f"<span style='color: {player.group.ball_color}'>{player.group.ball_color}</span> ball is drawn",
        ]
        if player.group.ball_color == C.R:
            b.append(f"Sender's choice: <br>&nbsp;Send \"<span class='red'>Ball is Red</span>\" with {player.group.if_red_send_red}% chance <br>&nbsp;Send \"<span class='blue'>Ball is Blue</span>\" with {player.group.if_red_send_blue}% chance")
        else:
            b.append(f"Sender's choice: <br>&nbsp;Send \"<span class='red'>Ball is Red</span>\" with {player.group.if_blue_send_red}% chance <br>&nbsp;Send \"<span class='blue'>Ball is Blue</span>\" with {player.group.if_blue_send_blue}% chance")

        b.append(f"Message sent to receiver = \"<span style='color: {player.group.message_sent}'>Ball is {player.group.message_sent}</span>\"")

        if form_elements == 4:
            if player.group.field_maybe_none('message_flagged') == None:
                b.append("Message is true. Cannot get flagged.")
            elif player.group.message_flagged:
                b.append("<span class='flagged'>Message Flagged! &#9873;</span>")
            else:
                b.append("<span class='notFlagged'>Message Not Flagged!</span>")

        b.append(f"Receiver’s guess = <span class='{player.group.guess}'>{player.group.guess}</span>")

        b.append(f"Sender earns {player.group.sender_payoff} (because Receiver guessed <span class='{player.group.guess}'>{player.group.guess}</span>)<br>Receiver earns {player.group.receiver_payoff} (because guess was {'correct' if player.group.ball_color == player.group.guess else 'incorrect'})")

        return dict(
                    form_elements= 4 if player.session.config["flagged"] > 0 else 2,
                    loading=a, 
                    final=b
                )

page_sequence = [PostPracticeWait, CommunicationStage, Wait1, GuessingStage, Wait2, LoadingPage, Summary]