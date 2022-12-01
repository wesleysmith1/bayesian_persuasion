from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'instructions0'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    quiz_attempts = models.IntegerField(initial=0)
    q1 = models.StringField(
            label="<b>Question 1:</b> What is the probability that a blue ball will be drawn?",
            choices=["0%", "25%", "33%", "50%", "67%", "75%", "100%"]
        )
    q2 = models.StringField(
        widget=widgets.RadioSelect,
        label="""<b>Question 2:</b> Suppose that the <b>Sender</b> chooses the following <i>Communication Plan</i>.<br><br>
        &emsp;&emsp;<i>If a red ball is drawn, then send the message “the ball is red” with a probability of 90%</i><br>
        &emsp;&emsp;<i>If a blue ball is drawn, then send the message “the ball is red” with a probability of 10%</i><br><br>
        Then, regardless of the color of the ball drawn,""",
        choices=[
            "(a) The message “the ball is red” will be sent with a probability of 90%",
            "(b) The message “the ball is blue” will be sent with a probability of 90%",
            "(c) The message will be true with a probability of 90%",
            "(d) The message will be false with a probability of 90%",
            "(e) None of the above"
        ]
    )

    q3 = models.StringField(
        widget=widgets.RadioSelect,
        label="""<b>Question 3:</b> Suppose that the <b>Sender</b> chooses the following <i>Communication Plan</i>. <br><br>
        &emsp;&emsp;<i>If a red ball is drawn, then send the message “the ball is red” with a probability of <u>100%</u></i><br>
        &emsp;&emsp;<i>If a blue ball is drawn, then send the message “the ball is red” with a probability of <u>0%</u></i><br><br>
        Then, regardless of the color of the ball drawn,""",
        choices=[
            "(a) The message “the ball is red” will be sent",
            "(b) The message “the ball is blue” will be sent",
            "(c) The message sent will be true",
            "(d) The message sent will be false",
        ]
    )

    q4a = models.StringField(
        label="""
        <b>Sender's</b> earnings =
        """,
        choices=["$0", "$2"]
    )

    q4b = models.StringField(
        label=
        """
        <b>Receiver's</b> earnings =
        """,
        choices=["$0", "$2"]
    )

# PAGES
class Instructions(Page):
    form_model = "player"
    form_fields = ["q1", "q2", "q3", "q4a", "q4b"]

    @staticmethod
    def error_message(player, values):

        player.quiz_attempts += 1

        solutions = dict(
            q1="67%",
            q2="(c) The message will be true with a probability of 90%",
            q3="(c) The message sent will be true",
            q4a="$0",
            q4b="$0",
            q5="(a) It is definitely false",
            q6="(c) It may be true or false",
            q7="(d) No, because 3 is not possible.",

        )

        question_labels = dict(
            q1=1,
            q2=2,
            q3=3,
            q4a=4,
            q4b=4,
            q5=5,
            q6=6,
            q7=7,

        )

        incorrect = []

        for field_name in values:
            if values[field_name] != solutions[field_name]:
                incorrect.append(question_labels[field_name])

        if len(incorrect):
            return f"You got the following question{'s' if len(incorrect)-1 else ''} wrong: {str(set(incorrect))[1:-1]}. Please try again."

    @staticmethod
    def vars_for_template(player: Player):
        flagged = int(player.session.config["flagged"] * 100)
        unflagged = 100 - flagged
        return dict(flagged=flagged, unflagged=unflagged)

    
class QuizCompleted(Page):
    pass


page_sequence = [ Instructions, QuizCompleted ]
