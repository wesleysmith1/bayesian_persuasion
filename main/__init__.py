from otree.api import *

import random

doc = """
Your app description
"""

class PostPracticeWait(WaitPage):
    wait_for_all_groups = True
    

class C(BaseConstants):
    NAME_IN_URL = 'main'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1

    SENDER_ROLE='sender'
    RECEIVER_ROLE='receiver'

    R = 'Red'
    B = 'Blue'

    PROBABILITY_BLUE = 67
    PROBABILITY_RED = 33

    CHART_TEMPLATE = 'main/chart.html'
    LOADING_TEMPLATE = 'main/loading.html'

    ROUND_PAY = cu(2)

    LOADING_INTERVAL = 5000 #3000

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


class Player(BasePlayer):
    pass


# FUNCTIONS
def creating_session(subsession: Subsession):
    subsession.group_randomly(fixed_id_in_group=True)


# PAGES
class CommunicationStage(Page):
    form_model = 'group'
    form_fields = ['if_red_send_red', 'if_red_send_blue', 'if_blue_send_red', 'if_blue_send_blue']

    @staticmethod
    def is_displayed(player: Player):
        return player.role == C.SENDER_ROLE

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

        sender = group.get_player_by_id(1)
        receiver = group.get_player_by_id(2)

        # payoffs
        if group.guess == C.R:
            sender.payoff = C.ROUND_PAY

        if group.ball_color == group.guess:
            receiver.payoff = C.ROUND_PAY


class GuessingStage(Page):
    form_model = 'group'

    @staticmethod
    def get_form_fields(player):
        if player.session.config["flagged"] > 0:
            return ['if_red_guess', 'if_red_flagged_guess', 'if_blue_guess', 'if_blue_flagged_guess']
        else:
            return ['if_red_guess', 'if_blue_guess']
    
    @staticmethod
    def is_displayed(player: Player):
        return player.role == C.RECEIVER_ROLE

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
        chart_title = "Sender's Communication Plan" if player.role == C.RECEIVER_ROLE else "You chose this Communication Plan"
        return dict(
                opponent_payoff=player.get_others_in_group()[0].payoff,
                chart_title=chart_title,
            )


class LoadingPage(Page):
    @staticmethod
    def vars_for_template(player: Player):
        a = [
                "Drawing a ball from bag", 
                "Looking at Sender’s Action Plan", 
                "Generating message with these probabilities", 
                "Message is going through Flagging Device",
                "Looking at Receiver’s Action Plan",
                "Calculating payoffs"
            ]
        b = [
            f"<span style='color: {player.group.ball_color}'>{player.group.ball_color}</span> ball is drawn",
        ]
        if player.group.ball_color == C.R:
            b.append(f"Sender's choice: <br>&nbsp;Send \"Ball is Red\" with {player.group.if_red_send_red}% chance <br>&nbsp;Send \"Ball is Blue\" with {player.group.if_red_send_blue}% chance")
        else:
            b.append(f"Sender's choice: <br>&nbsp;Send \"Ball is Red\" with {player.group.if_blue_send_red}% chance <br>&nbsp;Send \"Ball is Blue\" with {player.group.if_blue_send_blue}% chance")

        b.append(f"Message sent to receiver = \"Ball is <span style='color: {player.group.message_sent}'>{player.group.message_sent}</span>\"")

        if player.group.message_flagged == None:
            b.append("Message is true. Cannot get flagged.")
        elif player.group.message_flagged:
            b.append("<span class='notFlagged'>Message Not Flagged!</span>")
        else:
            b.append("<span class='flagged'>Message Flagged! &#9873;</span>")

        b.append(f"Receiver’s guess = {player.group.guess}")

        sender = player.group.get_player_by_role(C.SENDER_ROLE)
        receiver = player.group.get_player_by_role(C.RECEIVER_ROLE)
        b.append(f"Sender earns {sender.payoff} (because receiver guessed {player.group.guess})<br>Receiver earns {receiver.payoff} (because guess was {'correct' if player.group.ball_color == player.group.guess else 'incorrect'})")

        return dict(loading=a, final=b)

page_sequence = [PostPracticeWait, CommunicationStage, Wait1, GuessingStage, Wait2, LoadingPage, Summary]