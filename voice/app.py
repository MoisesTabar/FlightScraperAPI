import os
import tempfile
from fastapi import FastAPI, UploadFile
from dotenv import load_dotenv

from voice.voice import VoiceRecognitionService
from voice.models import VoiceSearchResponse
from voice.constants import API_DESCRIPTION, API_RESPONSES
from voice.middleware import register_exception_handlers

from openai import OpenAI

load_dotenv()

app = FastAPI(
    title="Voice Flight Search API",
    description="API for voice-based flight search using OpenAI Whisper and GPT-4",
    version="1.0.0"
)

register_exception_handlers(app)

voice_service = VoiceRecognitionService(
    client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
)

@app.post(
    "/voice/search",
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
