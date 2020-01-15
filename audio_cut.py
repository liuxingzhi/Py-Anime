from pydub import AudioSegment, effects
import os

audio = AudioSegment.from_file("src/videoplayback.webm")
# effects.speedup(audio[6 * 1000:-16 * 1000], playback_speed=1.10).export("src/卷珠帘琵琶吉他1.10.mp3", format="mp3")
# effects.speedup(audio[6 * 1000:-16 * 1000], playback_speed=1.15).export("src/卷珠帘琵琶吉他1.15.mp3", format="mp3")
# effects.speedup(audio[6 * 1000:-16 * 1000], playback_speed=1.20).export("src/卷珠帘琵琶吉他1.20.mp3", format="mp3")
# effects.speedup(audio, playback_speed=1.25).export("src/卷珠帘琵琶吉他1.25.mp3", format="mp3")
# effects.speedup(audio, playback_speed=1.30).export("src/卷珠帘琵琶吉他1.30.mp3", format="mp3")
audio[6 * 1000:-16 * 1000].export("src/卷珠帘琵琶吉他.mp3", format="mp3")
