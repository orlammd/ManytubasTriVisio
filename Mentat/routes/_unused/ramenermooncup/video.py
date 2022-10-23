from ..base import mk2_button, pedalboard_button
from modules import *

class Video():

    @pedalboard_button(10)
    def light_video(self):
        print('call from VIDEO')
