from threading import Thread
from pydub import AudioSegment
from pydub.playback import play
from time import sleep


class LoopMusic(Thread):
    def __init__(self, music, loop=1, interval=3, forever=False):
        super(LoopMusic, self).__init__()
        self.audio = music
        self.interval = interval
        if forever:
            self.loop = float("inf")
        else:
            self.loop = loop

    def run(self):
        while self.loop >= 1:
            play(self.audio)
            self.loop -= 1
            sleep(self.interval)


class BackgroundMusic:
    def __init__(self, song_name: str, loop=1, interval=3, forever=True):
        self.song_name = song_name
        self.music = AudioSegment.from_file(song_name)
        self.thread = LoopMusic(self.music, loop=loop, interval=interval, forever=forever)
        self.thread.setDaemon(True)

    def run(self):
        self.thread.start()

    def __enter__(self):
        self.run()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
