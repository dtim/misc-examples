import os
import sys
import time
from gtts import gTTS


def current_timestamp():
    millis = int(round(time.time() * 1000))
    return millis


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--lang", type=str, default="en", help="language")
    args = parser.parse_args()

    prefix = "tts_{}_".format(current_timestamp())
    number = 0
    for line in sys.stdin:
        number += 1
        tts = gTTS(line, lang=args.lang)
        tts.save(os.path.join("audio", "{}{:03d}.mp3".format(prefix, number)))


if __name__ == "__main__":
    main()
    print("Done!")
