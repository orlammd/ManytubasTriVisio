from ..base import mk2_button, pedalboard_button
from modules import *

class Light():

    @pedalboard_button(10)
    def light_test(self):
        print('call from LIGHT')
