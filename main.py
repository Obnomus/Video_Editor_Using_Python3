from moviepy.editor import *
import pandas as pd
from math import ceil
import moviepy.audio.fx.all as afx
import gtts
import os

f=pd.read_csv('clip_detail.csv')
no_of_clips = f.shape[0]

au=pd.read_csv('text2speech.csv')
#print(au)

Original_Audio_Scale_factor = 0.09
Speech_Audio_Scale_factor   = 0.1

clip=[]
for i in range(no_of_clips):
    clip.append( VideoFileClip(f['directory'][i]).subclip(f['start_time'][i],f['stop_time'][i])  )
    #audio.append(clip[i].audio)

video_clips=[clip[0].crossfadeout(2)]
idx= clip[0].duration
for vid in clip[1:]:
    video_clips.append( ((vid.set_start(idx).crossfadein(2)).set_position('center','top')).crossfadeout(2) )
    idx+=vid.duration


finalclip = CompositeVideoClip( video_clips )

main_audio=finalclip.audio
#main_audio.write_audiofile("Moviepy_Practice/Original_Audio.mp3",fps=44100)

audio_clips=[]
no_of_spl=au.shape[0]
tt=0
for j in range( no_of_spl ):
    myobj = gtts.gTTS(text=au['text2convert'][j], lang='en', slow=False, tld='co.in')
    myobj.save(f"Moviepy_Practice/txt_speech_{j+1}.mp3")
    speech = AudioFileClip(f"Moviepy_Practice/txt_speech_{j+1}.mp3")
    b=ceil(speech.duration)

    audio_clips.append(   (afx.audio_fadeout(afx.audio_fadein(main_audio.subclip(tt , au['time2attach'][j]), 2),1.5)).set_start(tt)  )
    audio_clips.append(  speech.set_start(au['time2attach'][j])   )
    tt+=(b+audio_clips[j*2].duration)
    audio_clips[-2] = afx.volumex(audio_clips[-2] , Original_Audio_Scale_factor)
    audio_clips[-1] = afx.volumex(audio_clips[-1] , Speech_Audio_Scale_factor)
    #audio_clips[j].write_audiofile(f"Moviepy_Practice/clip{j+1}.mp3",fps=44100)
    
    
audio_clips.append( (main_audio.subclip(tt , main_audio.duration )).set_start(tt) )
audio_clips[-1] = afx.volumex(audio_clips[-1] , Original_Audio_Scale_factor)
#main_audio.subclip(tt , main_audio.duration ).write_audiofile(f"Moviepy_Practice/clip{no_of_spl+1}.mp3",fps=44100)


final_aud = CompositeAudioClip(audio_clips)
#final_aud.write_audiofile(f"Moviepy_Practice/final_audio.mp3",fps=44100)

finalclip=finalclip.set_audio(final_aud)
finalclip.write_videofile('Output_Video.mp4')

for j in range( no_of_spl ):
    os.remove(f"Moviepy_Practice/txt_speech_{j+1}.mp3")
for i in clip:
    i.close()
for j in audio_clips:
    j.close()
