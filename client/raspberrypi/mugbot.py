import jtalk
import julius
from datetime import datetime
from mugbot_expression import get_mugbot_expression


class Mugbot(object):

    def __init__(self):
        self.exp = get_mugbot_expression
        self.__last_serif = None
        self.__last_serif_time = None

        self.__say("おはよう")

    def hear(self, message):
        if message[0:2]=="@x":
            angle = message[2:]
            if angle.isdigit():
                self.exp.nod_head(angle)

        elif message[0:2]=="@y":
            angle = message[2:]
            if angle.isdigit():
                self.exp.shake_head(angle)

        elif message[0:2]=="@z":
            brightness = message[2:]
            if brightness.isdigit():
                self.exp.brighten_eyes(brightness)

        elif message[0:2]=="@a":
            self.__listen()

        elif message[0:1]=="@":
            action = message[1:]
            if action.isalnum():
                self.exp.act_something(action)

        else:
            self.__say(message)

    def __act_something(self, action):
        self.exp.act_something(action)

    def __listen(self):
        self.__say('どうしました？')
        self.__act_something('w')
        user_utt = julius.julius()
        if not user_utt:
            self.__say('なるほど、{}ですね。'.format(user_utt))
        else:
            self.__say('ごめんなさい。聞き取れませんでした。')


    def __say(self, serif):
        self.__forget_last_serif()

        if not serif == self.__last_serif:
            self.exp.flash_eyes()
            jtalk.jtalk(serif)
            print("mugbot: {}".format(serif))
            self.exp.lighten_eyes()

            self.__last_serif = serif
            self.__last_serif_time = datetime.now()

    def __forget_last_serif(self):
        if not self.__last_serif_time is None:
            past_seconds = (datetime.now() - self.__last_serif_time).total_seconds()
            if past_seconds > 2:
                self.__last_serif = None
                self.__last_serif_time = None


get_mugbot = Mugbot()
