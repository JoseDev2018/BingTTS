# -*- coding: utf-8 -*-
"""

   A library to use the REST API of Azure Cloud Services - Text-To-Speech

"""
import requests


class BingTTS:

    def __init__(self, key_api=None):
        self.base_url = "https://westus.tts.speech.microsoft.com/cognitiveservices/v1"
        self.token_url = "https://westus.api.cognitive.microsoft.com/sts/v1.0/issueToken"
        self.payload = "<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='{}'>" \
                       "<voice  name='Microsoft Server Speech Text to Speech Voice ({}, {})'>" \
                       "{}</voice></speak>"
        self.api_key = key_api
        self.token = None

    def get_token(self):
        """
        Get temporal access token from Azure
        :return: Text token to access
        """
        headers = {"Ocp-Apim-Subscription-Key": self.api_key}
        response_token = requests.post(self.token_url, headers=headers)
        if int(response_token.status_code) != 200:
            raise BingAuthException(response_token.content)
        else:
            return response_token.content

    def speak(self, language="en-US", voice="ZiraRUS", file_format="riff-8khz-8bit-mono-mulaw", text=None):
        """
        Call Bing API REST and retrieve audio file
        :param language: the language selected for the conversion
        :param voice: the selected voice for the conversion
        :param file_format: The audio format selected for the conversion
        :param text: The text that you want to convert to voice
        :return: The audio data received
        """
        voice_list = {
            "ar-EG": ["Hoda"],
            "ar-SA": ["Naayf"],
            "bg-BG": ["Hoda"],
            "ca-ES": ["HerenaRUS"],
            "cs-CZ": ["Jakub"],
            "da-DK": ["HelleRUS"],
            "de-AT": ["Michael"],
            "de-CH": ["Karsten"],
            "de-DE": ["Hedda", "HeddaRUS", "Stefan, Apollo"],
            "el-GR": ["Stefanos"],
            "en-AU": ["Catherine", "HayleyRUS"],
            "en-CA": ["Linda", "HeatherRUS"],
            "en-GB": ["Susan, Apollo", "HazelRUS", "George, Apollo"],
            "en-IE": ["Sean"],
            "en-IN": ["Heera, Apollo", "PriyaRUS", "Ravi, Apollo"],
            "en-US": ["ZiraRUS", "JessaRUS", "BenjaminRUS"],
            "es-ES": ["Laura, Apollo", "HelenaRUS", "Pablo, Apollo"],
            "es-MX": ["HildaRUS", "Raul, Apollo"],
            "fi-FI": ["HeidiRUS"],
            "fr-CA": ["Caroline", "HarmonieRUS"],
            "fr-CH": ["Guillaume"],
            "fr-FR": ["Julie, Apollo", "HortenseRUS", "Paul, Apollo"],
            "he-IL": ["Asaf"],
            "hi-IN": ["Kalpana, Apollo", "Kalpana", "Hemant"],
            "hr-HR": ["Matej"],
            "hu-HU": ["Szabolcs"],
            "id-ID": ["Andika"],
            "it-IT": ["Cosimo, Apollo"],
            "ja-JP": ["Ayumi, Apollo", "Ichiro, Apollo", "HarukaRUS", "LuciaRUS", "EkaterinaRUS"],
            "ko-KR": ["HeamiRUS"],
            "ms-MY": ["Rizwan"],
            "nb-NO": ["HuldaRUS"],
            "nl-NL": ["HannaRUS"],
            "pl-PL": ["PaulinaRUS"],
            "pt-BR": ["HeloisaRUS", "Daniel, Apollo"],
            "pt-PT": ["HeliaRUS"],
            "ro-RO": ["Andrei"],
            "ru-RU": ["Irina, Apollo", "Pavel, Apollo"],
            "sk-SK": ["Filip"],
            "sl-SI": ["Lado"],
            "sv-SE": ["HedvigRUS"],
            "ta-IN": ["Valluvar"],
            "th-TH": ["Pattara"],
            "tr-TR": ["SedaRUS"],
            "vi-VN": ["An"],
            "zh-CN": ["HuihuiRUS", "Yaoyao, Apollo", "Kangkang, Apollo"],
            "zh-HK": ["Tracy, Apollo", "TracyRUS", "Danny, Apollo"],
            "zh-TW": ["Yating, Apollo", "HanHanRUS", "Zhiwei, Apollo"]
        }
        formats_list = [
            "raw-16khz-16bit-mono-pcm",
            "riff-16khz-16bit-mono-pcm",
            "raw-8khz-8bit-mono-mulaw",
            "riff-8khz-8bit-mono-mulaw",
            "audio-16khz-128kbitrate-mono-mp3",
            "audio-16khz-64kbitrate-mono-mp3",
            "audio-16khz-32kbitrate-mono-mp3",
            "raw-24khz-16bit-mono-pcm",
            "riff-24khz-16bit-mono-pcm",
            "audio-24khz-160kbitrate-mono-mp3",
            "audio-24khz-96kbitrate-mono-mp3",
            "audio-24khz-48kbitrate-mono-mp3"
        ]
        if len(text) > 950:
            raise BingTextLongException("Input text is too long")
        elif not text:
            raise BingNoTextException("No input text")
        if not self.token:
            self.token = self.get_token()
        if language not in voice_list:
            raise BingLanguageException("{} language not avaliable".format(language))
        if voice not in voice_list[language]:
            raise BingLanguageException("{} language does not have {} voice".format(language, voice))
        if file_format not in formats_list:
            raise BingFormatException("Format not valid")
        headers = {"Content-type": "application/ssml+xml",
                   "X-Microsoft-OutputFormat": file_format,
                   "X-Search-AppId": "D9BD1436F82A7F8F5C775E37E80C8790",
                   "X-Search-ClientID": "EF828F621DEE0B05CF5A35D35472AE10",
                   "User-Agent": "BingTTS",
                   "Authorization": "Bearer {}".format(self.token.decode("utf-8"))}
        body = self.payload.format(language,
                                   language,
                                   voice,
                                   text)
        try:
            response = requests.post(self.base_url, headers=headers, data=body)
        except requests.exceptions.RequestException as err:
            raise BingRequestException("Request error: {}".format(err))
        if int(response.status_code) != 200:
            if int(response.status_code) == 401:
                self.token = None
                return self.speak(language=language,
                                  voice=voice,
                                  file_format=file_format,
                                  text=text)
            else:
                raise BingBadRequestException(response.status_code)
        elif int(response.status_code) == 200:
            header = response.headers.get("content-type").lower()
            if "text" in header or "html" in header:
                raise BingFileException("Audio file can not read")
            else:
                return response.content


class BingAuthException(Exception):
    def __init__(self, message):
        self.message = "{}".format(
            message
        )
        super(
            BingAuthException,
            self
        ).__init__(
            self.message
        )


class BingLanguageException(Exception):
    def __init__(self, message):
        self.message = "{}".format(
            message
        )
        super(
            BingLanguageException,
            self
        ).__init__(
            self.message
        )


class BingFormatException(Exception):
    def __init__(self, message):
        self.message = "{}".format(
            message
        )
        super(
            BingFormatException,
            self
        ).__init__(
            self.message
        )


class BingRequestException(Exception):
    def __init__(self, message):
        self.message = "{}".format(
            message
        )
        super(
            BingRequestException,
            self
        ).__init__(
            self.message
        )


class BingFileException(Exception):
    def __init__(self, message):
        self.message = "{}".format(
            message
        )
        super(
            BingFileException,
            self
        ).__init__(
            self.message
        )


class BingTextLongException(Exception):
    def __init__(self, message):
        self.message = "{}".format(
            message
        )
        super(
            BingTextLongException,
            self
        ).__init__(
            self.message
        )


class BingBadRequestException(Exception):
    def __init__(self, message):
        self.message = "{}".format(
            message
        )
        super(
            BingBadRequestException,
            self
        ).__init__(
            self.message
        )


class BingNoTextException(Exception):
    def __init__(self, message):
        self.message = "{}".format(
            message
        )
        super(
            BingNoTextException,
            self
        ).__init__(
            self.message
        )
