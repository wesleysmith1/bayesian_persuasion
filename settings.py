from os import environ


SESSION_CONFIGS = [
    dict(
        display_name="main .5", name="main_5", app_sequence=['main', 'payment'], num_demo_participants=2, flagged=.5,
    ),
    dict(
        display_name="main .75", name="main_75", app_sequence=['main', 'payment'], num_demo_participants=2, flagged=.75,
    ),
    dict(
        display_name="main .25", name="main_25", app_sequence=['main', 'payment'], num_demo_participants=2, flagged=.25,
    ),
    dict(
        display_name="main 0", name="main_0", app_sequence=['main', 'payment'], num_demo_participants=2, flagged=0,
    ),
    dict(
        display_name="payment", name="payment", app_sequence=['payment'], num_demo_participants=1,
    ),
    dict(
        display_name="instructions", name="instructions", app_sequence=['instructions'], num_demo_participants=1, flagged=.5
    )
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=7.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

ROOMS = [
    dict(
        name='econ101',
        display_name='Econ 101 class',
        participant_label_file='_rooms/econ101.txt',
    ),
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '5535799752508'

INSTALLED_APPS = ['otree']
