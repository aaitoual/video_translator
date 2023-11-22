

import settings;
import utils;

import requests
from moviepy.editor import VideoFileClip
import random
from moviepy.editor import *
import moviepy.editor as mp
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip
import re
import codecs

from download import Download;
from converter import Converter
from transcribe import Transcribe
from translate  import Translator
import json

from speech import Speech
import os
from moviepy.config import change_settings

# Replace 'path_to_convert.exe' with the actual path to the ImageMagick convert.exe file
image_magick_path = 'C:\Program Files\ImageMagick-7.1.1-Q16\magick.exe'

if os.path.exists(image_magick_path):
    change_settings({"IMAGEMAGICK_BINARY": image_magick_path})
else:
    print("ImageMagick path not found. Please provide the correct path to the convert.exe file.")
os.environ["FFMPEG_BINARY"] = "C:/Program Files/FFmpeg/bin/ffmpeg.exe"


class VideoTranslate:

    def __init__(self, settings: any) -> None:
        self.settings = settings
    

    def translate_from_url(self, target_language, voice, final_name, translation_language, option):

        if (option == 1) :
            self.__get_url_from_video()

            video_path = self.__download_video()
            mp3_file   = self.__get_mp3_from_mp4(video_path)
            self.__wait_upload()
            # transcribe = self.__get_text_from_audio(mp3_file)
        transcribe = self.__get_text_from_long_audio(settings.VIDEOS_PATH + "audio1.mp3", "en-US")
        # translated = self.__translate_text(transcribe, target_language)
        translated = self.translate_long(transcribe, translation_language).replace('\n', '').replace('\r', '');

        self.__translated_to_speech(translated, voice)
        self.__wait_upload()
        subtitle = self.__get_text_from_long_audio(settings.VIDEOS_PATH + "audio2.mp3", target_language, 2)
        # with open('tmp.txt', 'w', encoding='utf-8') as srt_file:
        #     srt_file.write(json.dumps(subtitle))
        self.convert_to_srt(subtitle, settings.VIDEOS_PATH + "subtitle_" + target_language + ".srt" )
        self.__create_the_new_video(settings.VIDEOS_PATH + final_name, settings.VIDEOS_PATH + "audio2.mp3", settings.VIDEOS_PATH + "video_background.mp4")
        # # self.__change_audio_from_video_to_translated(video_path, settings.VIDEOS_PATH + final_name, settings.VIDEOS_PATH + "audio2.mp3")

        # final_message = "[{}] has been successfully translated"
        # print(final_message.format(self.video_url))

    def __wait_upload(self):
        input("Press Enter to continue...")
        print("Continuing after Enter was pressed")

    def convert_time_format(self,pt_time):
        total_seconds = 0

        if 'PT' in pt_time and 'S' in pt_time:
            time_parts = pt_time.split('PT')[1].split('S')[0]
            if time_parts:
                if 'H' in time_parts:
                    total_seconds += int(time_parts.split('H')[0]) * 3600
                    time_parts = time_parts.split('H')[1]
                if 'M' in time_parts:
                    total_seconds += int(time_parts.split('M')[0]) * 60
                    time_parts = time_parts.split('M')[1]
                if time_parts:
                    total_seconds += float(time_parts)

        milliseconds = int((total_seconds % 1) * 1000)
        total_seconds = int(total_seconds)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"
    
    def print_large_text(self, text):
        for char in text:
            if char == ' ':
                print(' ' * 8)  # Print spaces with a larger gap
            else:
                print(char * 8)  # Print each character multiple times to create a larger effect

    def convert_to_srt(self, json_data, path):
        data = json.loads(json.dumps(json_data))

        srt_content = ''
        index = 1

        for item in data:
            offset = self.convert_time_format(item['offset'])
            end_time = self.convert_time_format(f"PT{float(item['offsetInTicks'] + item['durationInTicks']) / 10000000:.2f}S")
            start_time = offset
            end_time = self.convert_time_format(f"PT{float(item['offsetInTicks'] + item['durationInTicks']) / 10000000:.2f}S")
            text = item['nBest'][0]['display']
            srt_content += f"{index}\n{start_time} --> {end_time}\n{text}\n\n"
            index += 1

        # Write the content to an SRT file
        with open(path, 'w', encoding='utf-8') as srt_file:
            srt_file.write(srt_content)




    # def get_subtitle(self, audio_path) :

    
    def __create_the_new_video(self, final_path, audio_path, video_path) :
        video = VideoFileClip(video_path)
        audioFile =  AudioFileClip(audio_path)
        video = video.set_audio(None)
        print ("___________")
        print (audioFile.duration)
        start_time = random.uniform(0, video.duration - audioFile.duration)
        short_video = video.subclip(start_time, start_time + audioFile.duration)
        middle_x = short_video.size[0] // 3
        cropped_clip = short_video.crop(x1=middle_x, y1=0, x2=2 * middle_x, y2=short_video.size[1])
        resized_clip = cropped_clip.resize(height=1920, width=1080)
        resized_clip = resized_clip.set_audio(audioFile)
        # subtitle_texts = [phrase['nBest'][0]['display'] for phrase in subtitles['recognizedPhrases']]
        # subtitle_durations = [phrase['duration'] for phrase in subtitles['recognizedPhrases']]
        # subtitle_seconds = [self.iso8601_to_seconds(duration) for duration in subtitle_durations]

        # Create TextClip for each subtitle and add it to the video
        # text_clips = []
        # for i, (text, duration) in enumerate(zip(subtitle_texts, subtitle_seconds)):
        #     text_clip = TextClip(text, fontsize=50, color='white', bg_color='black').set_position(('center', 'bottom')).set_duration(duration)
        #     text_clips.append(text_clip)
        # final_clip = resized_clip

        # Overlay text_clips onto the final_clip
        # for text_clip in text_clips:
        #     overlay_clip = final_clip.set_duration(max(final_clip.duration, text_clip.end))
        #     overlay_clip = overlay_clip.set_audio(resized_clip.audio)
        #     overlay_clip = overlay_clip.set_position(('center', 'bottom'))

        #     # Overlay text_clip at the appropriate duration
        #     overlayed_text_clip = text_clip.set_start(overlay_clip.duration)
        #     overlayed_text_clip = overlayed_text_clip.set_duration(text_clip.duration)
        #     overlayed_text_clip = overlay_clip.set_audio(resized_clip.audio)

        #     overlay_clip = CompositeVideoClip([overlay_clip, overlayed_text_clip])

            # final_clip = overlay_clip

        # Write the final_clip with subtitles to the output file
        # final_clip.write_videofile(final_path)
        resized_clip.write_videofile(final_path)

    def test (self, text, target_language) :
        header = {
          'Ocp-Apim-Subscription-Key': '69f9a27354e64ee4b7b5e74973d1108b',
          'Ocp-Apim-Subscription-Region': 'southafricanorth',
          "Content-Type": "application/json"
        }
        
        url = f'https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to={target_language}&from=en'
        
        ppayload = [{"Text": text}]
        
        res = requests.post(url, headers=header, json=ppayload);

        if (res.status_code != 200):
            print ("Error in the translation")
            exit (0)
        else :
            print ("translation done")
        return (res.json()[0]['translations'][0]['text'])

    def translate_long(self, transcribe, target_language):
        # start = 0
        # result: str = ""

        # while start < len(transcribe):
        #     end = start + 400

        #     if '.' in transcribe[start:end]:
        #         end = start + transcribe[start:end].rfind('.') + 1

        #     # Extract the substring
        #     substring = transcribe[start:end]

        #     # Process the substring (you can replace the print statement with your own function)
        #     result += self.__translate_text(transcribe[start:end], target_language)

        #     # Move to the next substring
        #     start = end
        result = self.test(transcribe, target_language);
        return result

    def __get_url_from_video(self) -> None:

        url = input("Please, type the video url: ");

        if(utils.is_url(url)):
             self.video_url = url
        else:
             print('the url is not valid');



    def __download_video(self) -> str:

        video_path = self.settings.VIDEOS_PATH

        if(self.video_url):

             video      = Download(video_path, self.video_url)
             video_path = video.dowload_YT()

             return video_path

            

    def __get_mp3_from_mp4(self, video_path: str) -> str:

        converter  = Converter(video_path);
        return converter.mp3_from_video(self.settings.VIDEOS_PATH)



    def __get_text_from_audio(self, file_mp3: str) -> str:
        
        assemblyAi_key = self.settings.ASSEMBLYAPI_KEY

        transcribe = Transcribe(assemblyAi_key)
        return transcribe.transcribe(file_mp3)
    
    def __get_text_from_long_audio(self, file_mp3: str, language, option=1) -> str:
        
        speechKey = self.settings.AZURE_SPEECH_SERVICE2

        transcribe = Transcribe(speechKey, self.settings.REGION2, "sttstorage1", "speechcontainer")
        return transcribe.transcribe_long(language, option)


    def __translate_text(self, text_to_translate: str, language: str) -> str:

        translator = Translator(text_to_translate)
        return translator.to(language)


    def __translated_to_speech(self, text: str, voice) -> None:

         azure_key = self.settings.AZURE_SPEECH_SERVICE
         azure_key2 = self.settings.AZURE_SPEECH_SERVICE2
         region= self.settings.REGION
         region2 = self.settings.REGION2

         speech  = Speech(azure_key, region, azure_key2, region2)
        #  speech.text_to_mp3(text, voice, self.settings.VIDEOS_PATH)
         speech.text_to_mp3_long(text, voice, self.settings.VIDEOS_PATH)


    def __change_audio_from_video_to_translated(self, video_path: str, final_name, audio_path) -> None:

         converter = Converter(video_path)
         converter.change_audio_from_video(audio_path, final_name)


def create_the_new_video(final_path, audio_path, video_path) :
        video = VideoFileClip(video_path)
        audioFile =  AudioFileClip(audio_path)
        video = video.set_audio(None)
        print ("___________")
        print (audioFile.duration)
        start_time = random.uniform(0, video.duration - audioFile.duration)
        short_video = video.subclip(start_time, start_time + audioFile.duration)
        middle_x = short_video.size[0] // 3
        cropped_clip = short_video.crop(x1=middle_x, y1=0, x2=2 * middle_x, y2=short_video.size[1])
        resized_clip = cropped_clip.resize(height=1920, width=1080)
        resized_clip = resized_clip.set_audio(audioFile)
        resized_clip.write_videofile(final_path)


video_translate = VideoTranslate(settings)

# video_translate.translate_from_url('ar-MA', "ar-MA-JamalNeural", "video-AR-MA.mp4", 'ar', 0)
video_translate.translate_from_url('ar-SA', "ar-SA-HamedNeural", "video-AR-SA.mp4", 'ar', 1)
video_translate.translate_from_url('pt-BR', "pt-BR-FranciscaNeural", "video-PT-BR.mp4", 'pt', 0)
video_translate.translate_from_url('fr-FR', "fr-FR-ClaudeNeural", "video-FR-FR.mp4", 'fr', 0)
video_translate.translate_from_url('es-MX', "es-MX-JorgeNeural", "video-ES-MX.mp4", 'fr', 0)
