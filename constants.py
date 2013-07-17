# Lemonade stand is Licensed under the Don't Be A Dick License
# (dbad-license). This license is an extension of the Apache License.
#
# If you do not wish to comply with the restrictions of the Don't Be A Dick
# License, this software is also available under the terms of the
# GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# The text of the Don't Be A Dick License is available at at
# <http://dbad-license.org/license>, while the GNU General Public License
# is available at <http://www.gnu.org/licenses/>.
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations # under the License.
#
# Authors:
#     Justin Lewis <jlew.blackout@gmail.com>
#     Nathaniel Case <Qalthos@gmail.com>

from gettext import gettext as _

STARTING_MONEY = [1500, 1250, 1000, 750]
STARTING_PRICE = 150
MAX_MSG = 18

# Dictionary of lists of the amount of starting items
# the player is given depending on difficulty
STARTING_ITEMS = {
    'lemonade': {
        'cup': [12, 10, 5, 0],
        'lemon': [18, 15, 5, 0],
        'sugar': [20, 10, 5, 0],
#        'strawberry': [18, 15, 5, 0]
    },
    'ice cream': {
        'cone': [12, 10, 5, 0],
        'ice cream': [18, 15, 2, 0],
        'sprinkles': [20, 10, 5, 0]
    },
    'noodle soup': {
        'bowl': [12, 10, 5, 0],
        'egg': [18, 15, 2, 0],
        'veggie': [20, 10, 5, 0]
    }
}

REP_VALUES = {
    'gain': [4, 3, 2, 1],
    'lose': [1, 1, 2, 2]
}

CHALLENGE_MODES = {

}

UPGRADES = {
    'lemonade': [
        {
            'name': _('Cooler'),
            'cost': 25,
            'capacity': 20,
            'level': 1,
            'saves': 'lemon',
            'info':
            [
                [
                    _("Stores lemons."),
                    _("Helps prevent lemons"),
                    _("from decaying.")
                ],
                [
                    _("Stores more lemons."),
                    _("Helps prevent animals"),
                    _("from stealing.")
                ],
                [
                    _("Stores more lemons.")
                ]
            ]
        },
        {
            'name': _('Sugar Jar'),
            'cost': 35,
            'capacity': 20,
            'level': 1,
            'saves': 'sugar',
            'info':
            [
                [
                    _("Stores sugar."),
                    _("Helps prevent ants"),
                    _("from stealing sugar.")
                ],
                [
                    _("Stores more sugar."),
                    _("Helps prevent sugar"),
                    _("from getting wet.")
                ],
                [
                    _("Stores more sugar.")
                ]
            ]
        },
        {
            'name': _('Cup Container'),
            'cost': 15,
            'capacity': 20,
            'level': 1,
            'saves': 'cup',
            'info':
            [
                [
                    _("Stores cups."),
                    _("Helps prevent wind"),
                    _("from blowing cups.")
                ],
                [
                    _("Stores more cups."),
                    _("Helps prevent cups"),
                    _("from breaking.")
                ],
                [
                    _("Stores more cups.")
                ]
            ]
        }
    ],
    'ice cream': [
        {
            'name': _('Cooler'),
            'cost': 2000,
            'capacity': 20,
            'level': 1,
            'saves': 'ice cream',
            'info':
            [
                [
                    _("Stores ice cream."),
                    _("Helps prevent ice"),
                    _("cream from melting")
                ],
                [
                    _("Stores more ice cream.")
                ]
            ]
        },
        {
            'name': _('Sprinkle Jar'),
            'cost': 1500,
            'capacity': 20,
            'level': 1,
            'saves': 'sprinkles',
            'info':
            [
                [
                    _("Stores sprinkles,"),
                    _("Helps prevent sprinkles"),
                    _("from being stolen.")
                ],
                [
                    _("Stores more sprinkles")
                ]
            ]
        }
    ],
    'noodle soup': [
        {
            'name': _('Cooler'),
            'cost': 2000,
            'capacity': 20,
            'level': 1,
            'saves': 'egg',
            'info':
            [
                [
                    _("Stores eggs."),
                    _("Helps prevent eggs"),
                    _("from going bad.")
                ],
                [
                    _("Stores more eggs.")
                ]
            ]
        },
        {
            'name': _('Veggie Jar'),
            'cost': 1500,
            'capacity': 20,
            'level': 1,
            'saves': 'veggie',
            'info':
            [
                [
                    _("Stores veggies,"),
                    _("Helps prevent veggies"),
                    _("from being stolen.")
                ],
                [
                    _("Stores more veggies")
                ]
            ]
        }
    ]
}

SERVING_ITEM = {
    'lemonade': _('cup'),
    'noodle soup': _('bowl'),
    'ice cream': _('cone')
}

ITEMS = {
    'lemonade': {
        'cup': {
            'name': _('Cup'),
            'cost': [5, 10, 15, 30],
            'decay': 0,
            'bulk': 1
        },
        'lemon': {
            'name': _('Lemons'),
            'cost': [15, 35, 55, 105],
            'decay': 5,
            'bulk': 1
        },
        'sugar': {
            'name': _('Sugar'),
            'cost': [2, 5, 8, 15],
            'decay': 0,
            'bulk': 1
        },
#        'strawberry': {
#            'name': _('Strawberry'),
#            'cost': [25, 50, 75, 150],
#            'decay': 3,
#            'bulk': 5
#        }
    },
    'ice cream': {
        'cone': {
            'name': _('Cone'),
            'cost': [5, 10, 15, 30],
            'decay': 0,
            'bulk': 1
        },
        'ice cream': {
            'name': _('Ice cream'),
            'cost': [15, 35, 55, 105],
            'decay': 5,
            'bulk': 1
        },
        'sprinkles': {
            'name': _('Sprinkle'),
            'cost': [2, 5, 8, 15],
            'decay': 0,
            'bulk': 1
        }
    },
    'noodle soup': {
        'bowl': {
            'name': _('Bowl'),
            'cost': [5, 10, 15, 30],
            'decay': 0,
            'bulk': 1
        },
        'egg': {
            'name': _('Egg'),
            'cost': [15, 35, 55, 105],
            'decay': 5,
            'bulk': 1
        },
        'veggie': {
            'name': _('Veggie'),
            'cost': [2, 5, 8, 15],
            'decay': 0,
            'bulk': 1
        }
    }
}

WEATHER = ["cloudy", "nice", "hot"]

BAD_ODDS = [5, 12, 38, 45]
GOOD_ODDS = [45, 38, 12, 5]

# Need to be in ascending order
EVENT_KEYS = ['20', '50', '80', '100']

B_EVENTS_DICT = {
    '20': {
        'lemonade': [
            {
                'text': _("A small animal takes some lemons!"),
                'item': 'lemon',
                'change': -2,
                'level': 2
            },
            {
                'text': _("A strong wind blows away some of your cups!"),
                'item': 'cup',
                'change': -2,
                'level': 1
            },
            {
                'text': _("Ants steal some of your supplies!"),
                'item': 'sugar',
                'change': -2,
                'level': 1
            }
        ]},
    '50': {
        'lemonade': [
            {
                'text': _("Your friend has eaten some of your lemons!"),
                'item': 'lemon',
                'change': 10,
                'level': 0
            },
            {
                'text': _("A batch of cups have cracked!"),
                'item': 'cup',
                'change': 10,
                'level': 2
            },
            {
                'text': _("You sneeze and blow away some sugar!"),
                'item': 'sugar',
                'change': 10,
                'level': 1
            }
        ]},
    '80': {
        'lemonade': [
            {
                'text': _("You sat on some of your lemons!"),
                'item': 'lemon',
                'change': 5,
                'level': 0
            },
            {
                'text': _("You stepped on some cups!"),
                'item': 'cup',
                'change': 5,
                'level': 2
            },
            {
                'text': _("Your sugar gets wet and ruined!"),
                'item': 'sugar',
                'change': 5,
                'level': 2
            }
        ]},
    '100': {
        'lemonade': [
            {
                'text': _("Some of your lemons are Lemonzilla eggs!"),
                'item': 'lemon',
                'change': 2,
                'level': 0
            },
            {
                'text': _("You mother takes some of your cups!"),
                'item': 'cup',
                'change': 2,
                'level': 0
            },
            {
                'text': _("You used too much sugar in one cup!"),
                'item': 'sugar',
                'change': 2,
                'level': 0
            }
        ]}
}

G_EVENTS_DICT = {
    '20': {
        'lemonade': [
            {
                'text': _("You find a baby Lemonzilla!"),
                'item': 'lemon',
                'change': -5
            },
            {
                'text': _("You rub a cup and your wish for cups is granted!"),
                'item': 'cup',
                'change': -5
            },
            {
                'text': _("A sugar farm would like to invest in your stand!"),
                'item': 'sugar',
                'change': -5
            }
        ]},
    '50': {
        'lemonade': [
            {
                'text': _("A lemon truck crashes in front of your stand!"),
                'item': 'lemon',
                'change': 100
            },
            {
                'text': _("It starts raining cups!"),
                'item': 'cup',
                'change': 100
            },
            {
                'text': _("You find a bag of sugar on the side of the road!"),
                'item': 'sugar',
                'change': 100
            }
        ]},
    '80': {
        'lemonade': [
            {
                'text': _("Your parents give you some lemons!"),
                'item': 'lemon',
                'change': 10
            },
            {
                'text': _("A friendly neighbor gives you some cups!"),
                'item': 'cup',
                'change': 10
            },
            {
                'text': _("A sugar salesman gives you some free samples!"),
                'item': 'sugar',
                'change': 10
            }
        ]},
    '100': {
        'lemonade': [
            {
                'text': _("You find extra lemons in your bag!"),
                'item': 'lemon',
                'change': 5
            },
            {
                'text': _("Something hits you in the back of the head!"),
                'item': 'cup',
                'change': 5
            },
            {
                'text':
                _("Some customers didn't notice you forgot the sugar!"),
                'item': 'sugar',
                'change': 5
            }
        ]}
}

LOCATIONS = {
    'neighborhood': {
        'base': 3,
        'multiple': 2,
        'cap': 50
    }
}

SCALE = [.2, .4, .6, .8]

#List of languages
LANGUAGE = [
    "English",
    "Espanol"
]

# List of difficulty types
DIFFICULTY = [
    _("Easy"),
    _("Normal"),
    _("Hard"),
    _("Impossible")
]

# List of menu items
MENU = [
    _("Play"),
    _("Challenge"),
    _("Tutorial")
]

# TODO: How to Localize data structures
CURRENCY = {
    _('Dollars'): 100,
    _('Quarters'): 25,
    _('Dimes'): 10,
    _('Nickels'): 5,
    _('Pennies'): 1
}

RECIPES = {
    'lemonade': {
        'basic': {
            'name': _("basic"),
            'cup': 1,
            'lemon': 2,
            'sugar': 3,
            'cost': [100, 175, 250, 350]
        },
        'sweet': {
            'name': _("sweet"),
            'cup': 1,
            'lemon': 1,
            'sugar': 10,
            'cost': [80, 175, 250, 356]
        },
        'fancy': {
            'name': _("fancy"),
            'cup': 3,
            'lemon': 2,
            'sugar': 1,
            'cost': [130, 190, 272, 393]
        },
        'juice': {
            'name': _("juice"),
            'cup': 1,
            'lemon': 5,
            'sugar': 5,
            'cost': [180, 380, 550, 800]
        },
        'epic': {
            'name': _("epic"),
            'cup': 2,
            'lemon': 3,
            'sugar': 5,
            'cost': [130, 275, 400, 550]
        }
    },
    'ice cream': {
        'basic': {
            'name': _("basic"),
            'cone': 1,
            'ice cream': 2,
            'sprinkles': 3,
            'cost': [100, 175, 250, 350]
        },
        'epic': {
            'name': _("epic"),
            'cone': 2,
            'ice cream': 3,
            'sprinkles': 5,
            'cost': [130, 275, 400, 550]
        }
    },
    'noodle soup': {
        'basic': {
            'name': _("basic"),
            'bowl': 1,
            'egg': 2,
            'veggie': 3,
            'cost': [100, 175, 250, 350]
        }
    }
}

import locale
locale.setlocale(locale.LC_ALL, '')


def format_money(value):
    return locale.currency(value / 100.0, grouping=True)
