from fortuneengine.GameEngine import GameEngine
from LemonadeMain import LemonadeMain
from LemonadeGui import LemonadeGui

ge = GameEngine(width=640, height=480, always_draw=False)
ge.add_object('main', LemonadeMain() )
ge.add_object('gui', LemonadeGui() )
ge.start_main_loop()
