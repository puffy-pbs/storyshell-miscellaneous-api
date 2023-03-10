from __future__ import annotations

import asyncio
import os

from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.params import Form

import whisper
from starlette.responses import FileResponse

from dto.audio_input_dto import AudioInputDto
from dto.presentation_input_dto import PresentationInputDto
from helpers.constants import DEFAULT_MODEL, DEFAULT_PRESENTATION_WIDTH, DEFAULT_PRESENTATION_HEIGHT
from helpers.miscellaneous import generate_save_filename, save_uploaded_file, generate_thumbnails

app = FastAPI()


@app.post("/thumbnails")
async def generate_thumbnails_from_presentation(
        presentation_file: UploadFile = None,
        width: int = Form(DEFAULT_PRESENTATION_WIDTH),
        height: int = Form(DEFAULT_PRESENTATION_HEIGHT)
):
    """
    Generate thumbnails from presentation file
    Args:
        presentation_file (UploadFile): The file that we should obtain the thumbnails from
        width (int): The desired width of the thumbnail (optional)
        height (int): The desired height of the thumbnail (optional)

    Raises:
        HTTPException

    Returns:
        FileResponse: Zip file response
    """
    try:
        # Validation
        dto = PresentationInputDto(presentation_file, width, height)

        # Where we will store the actual uploaded file
        output_filename = generate_save_filename(dto.presentation_file.filename)

        # Save the uploaded file
        await save_uploaded_file(output_filename, dto.presentation_file)

        # Get the loop
        loop = asyncio.get_running_loop()

        # Generate the thumbnails and the zip from them
        zip_file = await loop.run_in_executor(
            None,
            lambda: generate_thumbnails(
                output_filename,
                dto.width,
                dto.height
            )
        )

        # Generate file response
        return FileResponse(zip_file, media_type="application/octet-stream", filename="thumbnails.zip")
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except OSError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post("/transcribe")
async def transcribe_audio(audio_file: UploadFile = None, model: str = Form(DEFAULT_MODEL)) -> dict:
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
        output_filename = generate_save_filename(dto.audio_file.filename)

        # Save the uploaded file
        await save_uploaded_file(output_filename, dto.audio_file)

        # Get the loop
        loop = asyncio.get_running_loop()

        # Transcribe the audio
        transcribed_audio = await loop.run_in_executor(
            None,
            lambda: whisper.transcribe(
                whisper.load_model(dto.model),
                output_filename
            )
        )

        # Delete uploaded file
        os.remove(output_filename)

        # Generate the response
        return transcribed_audio
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")
