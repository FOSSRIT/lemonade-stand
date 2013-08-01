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

import gettext


class constants:

    def __init__(self, language):

        lang = gettext.translation(
            'org.laptop.Lemonade',
            'locale/',
            languages=[language])
        self._ = lang.ugettext

        self.starting_money = [1500, 1250, 1000, 750]
        self.starting_price = 150
        self.max_msg = 18

        # Dictionary of lists of the amount of starting items
        # the player is given depending on difficulty
        self.starting_items = {
            'lemonade': {
                'cup': [12, 10, 5, 0],
                'lemon': [18, 15, 5, 0],
                'sugar': [20, 10, 5, 0],
                #'strawberry': [0, 0, 0, 0],
                #'icecube': [0, 0, 0, 0]
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

        self.rep_values = {
            'gain': [4, 3, 2, 1],
            'lose': [1, 1, 2, 2]
        }

        self.challenge_mode = {

        }

        self.upgrades = {
            'lemonade': [
                {
                    'name': self._('Cooler'),
                    'cost': 25,
                    'capacity': 20,
                    'level': 1,
                    'saves': 'lemon',
                    'info':
                    [
                        [
                            self._("Stores lemons."),
                            self._("Helps prevent lemons"),
                            self._("from decaying.")
                        ],
                        [
                            self._("Stores more lemons."),
                            self._("Helps prevent animals"),
                            self._("from stealing.")
                        ],
                        [
                            self._("Stores more lemons.")
                        ]
                    ]
                },
                {
                    'name': self._('Sugar Jar'),
                    'cost': 35,
                    'capacity': 20,
                    'level': 1,
                    'saves': 'sugar',
                    'info':
                    [
                        [
                            self._("Stores sugar."),
                            self._("Helps prevent ants"),
                            self._("from stealing sugar.")
                        ],
                        [
                            self._("Stores more sugar."),
                            self._("Helps prevent sugar"),
                            self._("from getting wet.")
                        ],
                        [
                            self._("Stores more sugar.")
                        ]
                    ]
                },
                {
                    'name': self._('Cup Container'),
                    'cost': 15,
                    'capacity': 20,
                    'level': 1,
                    'saves': 'cup',
                    'info':
                    [
                        [
                            self._("Stores cups."),
                            self._("Helps prevent wind"),
                            self._("from blowing cups.")
                        ],
                        [
                            self._("Stores more cups."),
                            self._("Helps prevent cups"),
                            self._("from breaking.")
                        ],
                        [
                            self._("Stores more cups.")
                        ]
                    ]
                }
            ],
            'ice cream': [
                {
                    'name': self._('Cooler'),
                    'cost': 2000,
                    'prevents_losing': 'ice cream',
                    'capacity': 20,
                    'level': 1,
                    'saves': 'ice cream',
                    'info':
                    [
                        [
                            self._("Stores ice cream."),
                            self._("Helps prevent ice"),
                            self._("cream from melting")
                        ],
                        [
                            self._("Stores more ice cream.")
                        ]
                    ]
                },
                {
                    'name': self._('Sprinkle Jar'),
                    'cost': 1500,
                    'capacity': 20,
                    'level': 1,
                    'saves': 'sprinkles',
                    'info':
                    [
                        [
                            self._("Stores sprinkles,"),
                            self._("Helps prevent sprinkles"),
                            self._("from being stolen.")
                        ],
                        [
                            self._("Stores more sprinkles")
                        ]
                    ]
                }
            ],
            'noodle soup': [
                {
                    'name': self._('Cooler'),
                    'cost': 2000,
                    'capacity': 20,
                    'level': 1,
                    'saves': 'egg',
                    'info':
                    [
                        [
                            self._("Stores eggs."),
                            self._("Helps prevent eggs"),
                            self._("from going bad.")
                        ],
                        [
                            self._("Stores more eggs.")
                        ]
                    ]
                },
                {
                    'name': self._('Veggie Jar'),
                    'cost': 1500,
                    'capacity': 20,
                    'level': 1,
                    'saves': 'veggie',
                    'info':
                    [
                        [
                            self._("Stores veggies,"),
                            self._("Helps prevent veggies"),
                            self._("from being stolen.")
                        ],
                        [
                            self._("Stores more veggies")
                        ]
                    ]
                }
            ]
        }

        self.serving_item = {
            'lemonade': self._('cup'),
            'noodle soup': self._('bowl'),
            'ice cream': self._('cone')
        }

        self.items = {
            'lemonade': {
                'cup': {
                    'name': self._('Cup'),
                    'cost': [5, 10, 15, 30],
                    'decay': 0,
                    'bulk': 1,
                    'min': 1
                },
                'lemon': {
                    'name': self._('Lemon'),
                    'cost': [15, 35, 55, 105],
                    'decay': 5,
                    'bulk': 1
                },
                'sugar': {
                    'name': self._('Sugar'),
                    'cost': [2, 5, 8, 15],
                    'decay': 0,
                    'bulk': 1
                #},
                #'strawberry': {
                #    'name': self._('Strawberry'),
                #    'cost': [25, 50, 75, 150],
                #    'decay': 3,
                #    'bulk': 1
                #},
                #'icecube': {
                #    'name': self._('Ice Cube'),
                #    'cost': [1, 2, 5, 10],
                #    'decay': 0,
                #    'bulk': 1
                }
            },
            'ice cream': {
                'cone': {
                    'name': self._('Cone'),
                    'cost': [5, 10, 15, 30],
                    'decay': 0,
                    'bulk': 1,
                    'min': 1
                },
                'ice cream': {
                    'name': self._('Ice cream'),
                    'cost': [15, 35, 55, 105],
                    'decay': 5,
                    'bulk': 1
                },
                'sprinkles': {
                    'name': self._('Sprinkle'),
                    'cost': [2, 5, 8, 15],
                    'decay': 0,
                    'bulk': 1
                }
            },
            'noodle soup': {
                'bowl': {
                    'name': self._('Bowl'),
                    'cost': [5, 10, 15, 30],
                    'decay': 0,
                    'bulk': 1
                },
                'egg': {
                    'name': self._('Egg'),
                    'cost': [15, 35, 55, 105],
                    'decay': 5,
                    'bulk': 1
                },
                'veggie': {
                    'name': self._('Veggie'),
                    'cost': [2, 5, 8, 15],
                    'decay': 0,
                    'bulk': 1
                }
            }
        }

        self.weather = [self._("cloudy"), self._("nice"), self._("hot")]
        self.weather_name = ["cloudy", "nice", "hot"]

        self.bad_odds = [5, 12, 38, 45]
        self.good_odds = [45, 38, 12, 5]

        # Need to be in ascending order
        self.event_keys = ['20', '50', '80', '100']

        self.bad_event_dict = {
            '20': {
                'lemonade': [
                    {
                        'text': self._("A small animal takes some lemons!"),
                        'item': 'lemon',
                        'change': -2,
                        'level': 2
                    },
                    {
                        'text': self._(
                            "A strong wind blows away some of your cups!"),
                        'item': 'cup',
                        'change': -2,
                        'level': 1
                    },
                    {
                        'text': self._("Ants steal some of your supplies!"),
                        'item': 'sugar',
                        'change': -2,
                        'level': 1
                    }
                    #{
                    #    'text': self._("Your strawberries are infested!"),
                    #    'item': 'strawberry',
                    #    'change': -2
                    #},
                    #{
                    #    'text': self._("Your ice melts!"),
                    #    'item': 'icecube',
                    #    'change': -2
                    #}
                ]},
            '50': {
                'lemonade': [
                    {
                        'text': self._(
                            "Your friend has eaten some of your lemons!"),
                        'item': 'lemon',
                        'change': 10,
                        'level': 0
                    },
                    {
                        'text': self._("A batch of cups have cracked!"),
                        'item': 'cup',
                        'change': 10,
                        'level': 2
                    },
                    {
                        'text': self._("You sneeze and blow away some sugar!"),
                        'item': 'sugar',
                        'change': 10,
                        'level': 1
                    }
                    #{
                    #    'text': self._("A bird takes your strawberries!"),
                    #    'item': 'strawberry',
                    #    'change': 10
                    #},
                    #{
                    #    'text': self._("Your ice is contaminated!"),
                    #    'item': 'icecube',
                    #    'change': 10
                    #}
                ]},
            '80': {
                'lemonade': [
                    {
                        'text': self._("You sat on some of your lemons!"),
                        'item': 'lemon',
                        'change': 5,
                        'level': 0
                    },
                    {
                        'text': self._("You stepped on some cups!"),
                        'item': 'cup',
                        'change': 5,
                        'level': 2
                    },
                    {
                        'text': self._("Your sugar gets wet and ruined!"),
                        'item': 'sugar',
                        'change': 5,
                        'level': 2
                    }
                    #{
                    #    'text': self._("Your strawberries got trampled!"),
                    #    'item': 'strawberry',
                    #    'change': 5
                    #},
                    #{
                    #    'text': self._("Your friend eats some of your ice!"),
                    #    'item': 'icecube',
                    #    'change': 5
                    #}
                ]},
            '100': {
                'lemonade': [
                    {
                        'text': self._(
                            "Some of your lemons are Lemonzilla eggs!"),
                        'item': 'lemon',
                        'change': 2,
                        'level': 0
                    },
                    {
                        'text': self._("You mother takes some of your cups!"),
                        'item': 'cup',
                        'change': 2,
                        'level': 0
                    },
                    {
                        'text': self._("You used too much sugar in one cup!"),
                        'item': 'sugar',
                        'change': 2,
                        'level': 0
                    }
                    #{
                    #    'text': self._(
                    #    "Your friend eats some of your strawberries!"),
                    #    'item': 'strawberry',
                    #    'change': 2
                    #},
                    #{
                    #    'text': self._("Some ice cubes dissapeared!"),
                    #    'item': 'icecube',
                    #    'change': 2
                    #}
                ]}
        }

        self.good_event_dict = {
            '20': {
                'lemonade': [
                    {
                        'text': self._("You find a baby Lemonzilla!"),
                        'item': 'lemon',
                        'change': -5
                    },
                    {
                        'text': self._(
                            "You rub a cup and your"
                            "wish for cups is granted!"),
                        'item': 'cup',
                        'change': -5
                    },
                    {
                        'text': self._(
                            "A sugar farm would"
                            "like to invest in your stand!"),
                        'item': 'sugar',
                        'change': -5
                    }
                    #{
                    #    'text': self._("A happy customer give you a gift!"),
                    #    'item': 'strawberry',
                    #    'change': -5
                    #},
                    #{
                    #    'text': self._("It begins to hail!"),
                    #    'item': 'icecube',
                    #    'change': -5
                    #}
                ]},
            '50': {
                'lemonade': [
                    {
                        'text': self._(
                            "A lemon truck crashes in front of your stand!"),
                        'item': 'lemon',
                        'change': 100
                    },
                    {
                        'text': self._("It starts raining cups!"),
                        'item': 'cup',
                        'change': 100
                    },
                    {
                        'text': self._(
                            "You find a bag of sugar on the sidewalk!"),
                        'item': 'sugar',
                        'change': 100
                    }
                    #{
                    #    'text': self._("You find a strawberry bush!"),
                    #    'item': 'strawberry',
                    #    'change': 100
                    #},
                    #{
                    #    'text': self._("A restaurant wants to support you!"),
                    #    'item': 'icecube',
                    #    'change': 100
                    #}
                ]},
            '80': {
                'lemonade': [
                    {
                        'text': self._("Your parents give you some lemons!"),
                        'item': 'lemon',
                        'change': 10
                    },
                    {
                        'text': self._(
                            "A friendly neighbor gives you some cups!"),
                        'item': 'cup',
                        'change': 10
                    },
                    {
                        'text': self._(
                            "A sugar salesman gives you some free samples!"),
                        'item': 'sugar',
                        'change': 10
                    }
                    #{
                    #    'text': self._(
                    #    "Your friend brings you a gift to make up!"),
                    #    'item': 'strawberry',
                    #    'change': 10
                    #},
                    #{
                    #    'text': self._(
                    #       "You break your icecubes into smaller pieces!"),
                    #    'item': 'icecube',
                    #    'change': 10
                    #}
                ]},
            '100': {
                'lemonade': [
                    {
                        'text': self._("You find extra lemons in your bag!"),
                        'item': 'lemon',
                        'change': 5
                    },
                    {
                        'text': self._(
                            "Something hits you in the back of the head!"),
                        'item': 'cup',
                        'change': 5
                    },
                    {
                        'text': self._(
                            "Some customers didn't notice"
                            "you forgot the sugar!"),
                        'item': 'sugar',
                        'change': 5
                    }
                    #{
                    #    'text': self._("Free give away at the farm!"),
                    #    'item': 'strawberry',
                    #    'change': 5
                    #},
                    #{
                    #    'text': self._("A upset customer throws ice at you!"),
                    #    'item': 'icecube',
                    #    'change': 5
                    #}
                ]}
        }

        self.locations = {
            'neighborhood': {
                'base': 3,
                'multiple': 2,
                'cap': 50
            }
        }

        self.scale = [.2, .4, .6, .8]

        #List of languages
        self.language = [
            "English",
            "Espanol"
        ]

        # List of difficulty types
        self.difficulty = [
            self._("Easy"),
            self._("Normal"),
            self._("Hard"),
            self._("Impossible")
        ]

        # List of menu items
        self.menu = [
            self._("Play"),
            self._("Challenge"),
            self._("Tutorial")
        ]

        # TODO: How to Localize data structures
        self.currency = {
            self._('Dollars'): 100,
            self._('Quarters'): 25,
            self._('Dimes'): 10,
            self._('Nickels'): 5,
            self._('Pennies'): 1
        }

        self.recipes = {
            'lemonade': {
                'basic': {
                    'name': self._("basic"),
                    'cup': 1,
                    'lemon': 2,
                    'sugar': 3,
                    'cost': [100, 175, 250, 350]
                },
                'iced': {
                    'name': self._("iced"),
                    'cup': 1,
                    'lemon': 2,
                    'sugar': 3,
                    'icecube': 3,
                    'cost': [100, 200, 275, 390]
                },
                'icedjuce': {
                    'name': self._("iced juice"),
                    'cup': 1,
                    'strawberry': 2,
                    'sugar': 3,
                    'icecube': 3,
                    'cost': [130, 240, 340, 506]
                },
                'juice': {
                    'name': self._("juice"),
                    'cup': 1,
                    'strawberry': 2,
                    'sugar': 3,
                    'cost': [120, 230, 315, 470]
                },
                'strawberry': {
                    'name': self._("strawberry"),
                    'cup': 1,
                    'lemon': 2,
                    'sugar': 3,
                    'strawberry': 2,
                    'cost': [180, 350, 490, 731]
                },
                'icedstrawberry': {
                    'name': self._("iced strawberry"),
                    'cup': 1,
                    'lemon': 2,
                    'strawberry': 2,
                    'sugar': 3,
                    'icecube': 3,
                    'cost': [210, 365, 500, 820]
                },
                'epic': {
                    'name': self._("epic"),
                    'cup': 2,
                    'lemon': 3,
                    'sugar': 5,
                    'cost': [130, 275, 400, 550]
                },
                'custom': {
                    'name': self._("custom"),
                    'cost': [0, 0, 0, 0]
                }
            },
            'ice cream': {
                'basic': {
                    'name': self._("basic"),
                    'cone': 1,
                    'ice cream': 2,
                    'sprinkles': 3,
                    'cost': [100, 175, 250, 350]
                },
                'epic': {
                    'name': self._("epic"),
                    'cone': 2,
                    'ice cream': 3,
                    'sprinkles': 5,
                    'cost': [130, 275, 400, 550]
                },
                'custom': {
                    'name': self._("custom"),
                    'cost': [0, 0, 0, 0]
                }
            },
            'noodle soup': {
                'basic': {
                    'name': self._("basic"),
                    'bowl': 1,
                    'egg': 2,
                    'veggie': 3,
                    'cost': [100, 175, 250, 350]
                }
            }
        }

import locale
locale.setlocale(locale.LC_ALL, '')


CURRENCY = {
    'Dollars': 100,
    'Quarters': 25,
    'Dimes': 10,
    'Nickels': 5,
    'Pennies': 1
}


def format_money(value):
    return locale.currency(value / 100.0, grouping=True)
