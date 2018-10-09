# BingTTS
A wrapper to link python to the Bing REST API

# Example
```python
# -*- coding: utf-8 -*-
from bingtts import BingTTS
if __name__=='__main__':
    tts = BingTTS('[YOUR API KEY]')
    output = tts.speak(language='en-US',
                       voice='ZiraRUS',
                       file_format='audio-16khz-32kbitrate-mono-mp3',
                       text='Test of Bing text to speech')
    with open('file_name.mp3', 'wb') as file_mp3:
        file_mp3.write(output)
        file_mp3.close()
```
