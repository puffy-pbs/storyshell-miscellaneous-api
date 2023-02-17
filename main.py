from __future__ import annotations

import asyncio
import os.path
import random

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
        filename, extension = os.path.splitext(dto.audio_file.filename)
        rnd = random.randint(100, 100000)
        output_filename = "web/" + filename + str(rnd) + extension

        # Save the uploaded file
        async with aiofiles.open(output_filename, "wb") as out_file:
            content = await dto.audio_file.read()
            await out_file.write(content)

        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None,
            lambda: whisper.transcribe(
                whisper.load_model(dto.model),
                output_filename
            )
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")
