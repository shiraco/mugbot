import subprocess
from datetime import datetime


def jtalk(t):
    open_jtalk = ['open_jtalk']
    mech = ['-x', '/var/lib/mecab/dic/open-jtalk/naist-jdic']
    htsvoice = ['-m', '/usr/share/hts-voice/mei/mei_normal.htsvoice']
    speed = ['-r', '1.0']
    outwav = ['-ow', 'open_jtalk.wav']
    cmd = open_jtalk + mech + htsvoice + speed + outwav
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    out, err = proc.communicate(t.encode('utf-8'))
    proc.wait()

    aplay = ['aplay', '-q', 'open_jtalk.wav']
    wr = subprocess.Popen(aplay)
    wr.wait()

    rm = ['rm', '-f', 'open_jtalk.wav']
    rm_proc = subprocess.Popen(rm)
    rm_proc.wait()


def say_datetime():
    d = datetime.now()
    text = '%s月%s日、%s時%s分%s秒' % (d.month, d.day, d.hour, d.minute, d.second)
    jtalk(text)


if __name__ == '__main__':
    say_datetime()
