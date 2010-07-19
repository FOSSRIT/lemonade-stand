from fortuneengine.GameEngine import GameEngine
from LemonadeMain import LemonadeMain
from LemonadeGui import LemonadeGui
from optparse import OptionParser

parser = OptionParser()

parser.add_option("", "--width", dest="width", help="window width",
                  metavar="WIDTH", default=640, type="int")

parser.add_option("", "--height", dest="height", help="window height",
                  metavar="HEIGHT", default=480, type="int")

(opts, args) = parser.parse_args()

ge = GameEngine(width=opts.width, height=opts.height, always_draw=False)
ge.add_object('main', LemonadeMain() )
ge.add_object('gui', LemonadeGui() )
ge.start_main_loop()
