# video-translate

![python](https://img.shields.io/static/v1?label=Python&labelColor=07a0f8&message=v3.8.10&color=000000&logo=python&logoColor=ffffff&style=flat-square)
![python](https://img.shields.io/static/v1?label=pytube&labelColor=dd3838&message=v12.1.0&color=000000&logo=python&logoColor=ffffff&style=flat-square)
![azure ](https://img.shields.io/static/v1?label=Azure+TTS&labelColor=0778ba&message=+v3.0&color=000000&logo=azure+&logoColor=ffffff&style=flat-square)

A simplee and quick projecet about translating youtube shorts (working for casual and story shorts with no visual content)

### Basic usage:


~~~bash
    python3 translator/shorts-translator.py
~~~

<br>

### How it works? SIMPLE: 

<br>
    After downloading the youtube short provided by the link in the "links.txt" file, the program will substract the audio from that video and save it
    Then it will be uploaded to your azure storage container so it can be used to be transcribed (for short videos, i mean really short videos, ther's a simple way to skip this step and avoid using azure storage)
    <br>
    Then the program will craete a transcription request and wait for it to finish and get the text
    <br>
    Then using azure translator service the program will translate the text to the desired language from the desired language (from en to fr in the default case, please check the supported languages here <link> https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=stt </link>)
    <br>
    Then using the speech service again, the program will convert the translated text to a voice
    <br>
    Then we upload the new voice again to get the new translated text with the times to save it as an srt file for subtitle
    <br>
    Then the program will cut a random chunk from the "path_to_the_directery/translator/resources/video_background.mp4" video and add the audio to it then save it
    <br>
    Then all the files will be moved to /results folder
<br>


<br>
<br>
