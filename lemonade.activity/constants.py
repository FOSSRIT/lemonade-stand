# Lemonade stand is Licensed under the Don't Be A Dick License
# (dbad-license). This license is an extension of the Apache License.
#
# You may find a copy of this license at http://dbad-license.org/license
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
            'name':_('Cups'),
            'cost':10,
            'decay':0,
            'peritem':1,
            'bulk':12
            },
        'lemon': {
            'name':_('Lemons'),
            'cost':35,
            'decay':5,
            'peritem':2,
            'bulk':1
            },
        'sugar': {
            'name':_('Sugar'),
            'cost':5,
            'decay':0,
            'peritem':3,
            'bulk':100}
    }

WEATHER = {
    '-1': "Rainy",
    '0': "Nice",
    '1': "Hot"
}

# TODO: How to Localize data structures
CURRENCY = {
    'Dollars':100,
    'Quarters':25,
    'Dimes':10,
    'Nickels':5,
    'Pennies':1
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

