import os
import tempfile
from fastapi import APIRouter, UploadFile
from dotenv import load_dotenv

from voice.voice import VoiceRecognitionService
from voice.models import VoiceSearchResponse
from voice.constants import API_DESCRIPTION, API_RESPONSES
from scraper.scraper import search_flights

from openai import OpenAI

load_dotenv()

router = APIRouter()

voice_service = VoiceRecognitionService(
    client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
)

@router.post(
    "/search/voice",
    response_model=VoiceSearchResponse,
    responses=API_RESPONSES,
    description=API_DESCRIPTION
)
async def voice_search(
    audio: UploadFile
) -> VoiceSearchResponse:
    audio_content = await audio.read()
    
    # Create temporary file for audio processing
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=f"_{audio.filename}"
    ) as temp_file:
        temp_file.write(audio_content)
        temp_file.flush()
        temp_path = temp_file.name
    
    try:
        with open(temp_path, "rb") as audio_file:
            result = await voice_service.process_audio(
                file=audio_file,
                filename=audio.filename
            )
        
        return VoiceSearchResponse(**result)
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)
