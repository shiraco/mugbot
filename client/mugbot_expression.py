import serial


class MugbotExpression(object):

    def __init__(self, port="/dev/ttyACM0"):
        self.sp = serial.Serial(port, 9600)

    def flash_eyes(self):
        sp = self.sp
        sp.write("t".encode("utf-8"))

    def lighten_eyes(self):
        self.sp.write("n".encode("utf-8"))


get_mugbot_expression = MugbotExpression()
