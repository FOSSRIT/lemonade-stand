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
# specific language governing permissions and limitations
# under the License.
#
# Authors:
#     Justin Lewis <jlew.blackout@gmail.com>
#     Nathaniel Case <Qalthos@gmail.com>

from gettext import gettext as _

STARTING_MONEY = 1000
STARTING_PRICE = 150
MAX_MSG = 10
ITEMS = {
    'cup': {
        'name': _('Cups'),
        'cost': 10,
        'decay': 0,
        'bulk': 12
    },
    'lemon': {
        'name': _('Lemons'),
        'cost': 35,
        'decay': 5,
        'bulk': 1
    },
    'sugar': {
        'name': _('Sugar'),
        'cost': 5,
        'decay': 0,
        'bulk': 50
    },
#    'strawberry': {
#        'name': _('Strawberry'),
#        'cost': 50,
#        'decay': 3,
#        'bulk': 5
#    }
}

WEATHER = ["cloudy", "nice", "hot"]

EVENTS = [
    {'text': _("A lemon truck crashes in front of your stand!"),
     'item': 'lemon',
     'change': 10
    },
    {'text': _("It starts raining cups!"),
     'item': 'cup',
     'change': 10
    },
    {'text': _("Ants steal some of your supplies!"),
     'item': 'sugar',
     'change': -10
    },
    {'text': _("A sugar salesman gives you some free samples!"),
     'item': 'sugar',
     'change': 10
    }

]

DIFFICULTY = [
    "Easy",
    "Normal",
    "Hard",
    "Impossible"
]

# TODO: How to Localize data structures
CURRENCY = {
    'Dollars': 100,
    'Quarters': 25,
    'Dimes': 10,
    'Nickels': 5,
    'Pennies': 1
}

RECIPES = {
    'basic': {
        'cup': 1,
        'lemon': 2,
        'sugar': 3,
        'cost': 150
    },
    'strawberry': {
        'cup': 1,
        'lemon': 2,
        'sugar': 2,
        'strawberry': 1,
        'cost': 225
    },
    'epic': {
        'cup': 2,
        'lemon': 3,
        'sugar': 5,
        'cost': 500
    }
}

import locale
locale.setlocale(locale.LC_ALL, '')
def format_money(value):
    return locale.currency( value / 100.0, grouping=True )

