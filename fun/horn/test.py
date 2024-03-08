import pydub
from pydub import AudioSegment
import matplotlib.pyplot as plt
from scipy.io import wavfile
from tempfile import mktemp

mp3_audio = AudioSegment.from_file("/Users/gpeterson/Downloads/17974.mp3", format="mp3")  # read mp3
wname = mktemp('.wav')  # use temporary file
mp3_audio.export(wname, format="wav")  # convert to wav
FS, data = wavfile.read(wname)  # read wav file
spec, freq, times, im = plt.specgram(data[:,0], Fs=FS, NFFT=128, noverlap=0)  # plot
plt.show()
...
# if __name__=="__main__":
#     audio = pydub.AudioSegment.from_mp3("/Users/gpeterson/Downloads/17974.mp3")
#     ...