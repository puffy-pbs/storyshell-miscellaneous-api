from __future__ import annotations

import aiofiles as aiofiles
from fastapi import FastAPI, UploadFile, HTTPException

import whisper
from fastapi.params import Form

from audio_input_dto import AudioInputDto
from constants import DEFAULT_MODEL

transcript_generator = FastAPI()


@transcript_generator.post("/")
async def transcribe_audio(audio_file: UploadFile = None, model: str = Form(DEFAULT_MODEL)):
    """
    Transcribe audio and return it`s 'text', 'segments', 'language' properties
    Args:
        audio_file (UploadFile): The file that should be transcribed
        model (str): The model used ("tiny", "base", "small", "medium", "large")

    Raises:
        HTTPException

    Returns:
        dict: Object with 'text', 'segments', 'language' properties of the transcribed audio
    """
    try:
        # Validation
        dto = AudioInputDto(audio_file, model)

        # Where we will store the actual uploaded file
        output_filename = "web/" + dto.audio_file.filename

        # Save the uploaded file
        async with aiofiles.open(output_filename, "wb") as out_file:
            content = await dto.audio_file.read()
            await out_file.write(content)

        whisper_model = whisper.load_model(dto.model)

        # Transcribe using whisper
        return whisper.transcribe(whisper_model, output_filename)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")
