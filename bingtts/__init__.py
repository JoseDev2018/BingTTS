# -*- coding: utf-8 -*-
from .bingtts import BingTTS, BingBadRequestException, BingFormatException, BingLanguageException, BingAuthException,\
    BingFileException, BingNoTextException, BingRequestException, BingTextLongException
from .version import __version__
__all__ = ['BingTTS', 'BingBadRequestException', 'BingFormatException', 'BingLanguageException', 'BingAuthException',
           'BingFileException', 'BingNoTextException', 'BingRequestException', 'BingTextLongException']