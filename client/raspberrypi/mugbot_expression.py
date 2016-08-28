import serial
import time


class MugbotExpression(object):

    def __init__(self, port="/dev/ttyACM0"):
        self.sp = serial.Serial(port, 9600)

    def __express(self, exp):
        self.sp.write(exp.encode("utf-8"))
        time.sleep(0.01)

    def flash_eyes(self):
        self.__express("t")

    def lighten_eyes(self):
        self.__express("n")

    def nod_head(self, angle):
        self.__express("{}x".format(angle))

    def shake_head(self, angle):
        self.__express("{}y".format(angle))

    def brighten_eyes(self, brightness):
        self.__express("{}z".format(brightness))

    def act_something(self, action):
        self.__express("{}".format(action))


get_mugbot_expression = MugbotExpression()
