import subprocess


def record():
    cmd = ['arecord', '-D', 'plughw:1,0', '-t', 'wav', '-d', '2', '-f', 'S16_LE', '-r', '16000', 'record.wav']
    wr = subprocess.Popen(cmd)
    wr.wait()

def julius():
    record()

    t = 'record.wav'
    cmd = ['/home/pi/julius-4.3.1/julius/julius', '-C', '/home/pi/julius-kits/dictation-kit-v4.3.1-linux/main.jconf', '-C', '/home/pi/julius-kits/dictation-kit-v4.3.1-linux/am-gmm.jconf', '-nostrip', '-outfile', '-palign', '-input', 'file']
    env = {'ALSADEV': 'plughw:1,0', 'AUDIODEV': '/dev/dsp1'}
    proc = subprocess.Popen(cmd, env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate(t.encode('utf-8'))
    proc.wait()

    recognized = recognize()

    return recognized

def recognize():
    with open('record.out') as f:
        data = f.read()

    lines = data.split('\n')
    result = lines[0].replace("sentence1:", "")

    if result=="<search failed>":
        result = None
    elif len(result.strip())<3:
        result = None

    print(result)
    return result

if __name__ == "__main__":
    julius()
