from pydub import AudioSegment
import os

audio = AudioSegment.from_file("src/videoplayback.webm")
audio[6 * 1000:-16 * 1000].export("src/卷珠帘琵琶吉他.mp3", format="wav")
