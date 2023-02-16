from __future__ import annotations

from fastapi import UploadFile

from constants import VALID_MODELS


class AudioInputDto:
    """
    AudioInputDto`s main purpose is to validate and provide an easy-to-use wrapper of the values listed below

    Attributes:
        audio_file (UploadFile): The file that should be transcribed
        model (str): The model used ("tiny", "base", "small", "medium", "large")

    Raises:
        ValueError
    """
    audio_file: UploadFile
    model: str

    def __init__(self, file, model):
        if not isinstance(file.__class__, UploadFile.__class__):
            raise ValueError("File is not correct")
        self.audio_file = file

        if not isinstance(model, str) or model not in VALID_MODELS:
            raise ValueError("Model is not valid")
        self.model = model
