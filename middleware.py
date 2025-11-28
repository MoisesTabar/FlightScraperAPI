import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from voice.errors import (
    InvalidAudioFormatError,
    AudioFileTooLargeError,
    TranscriptionError,
    StructuredExtractionError,
    VoiceRecognitionError,
)

logger = logging.getLogger(__name__)


async def invalid_audio_format_handler(
    request: Request, exc: InvalidAudioFormatError
) -> JSONResponse:
    logger.warning(f"Invalid audio format: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "InvalidAudioFormat",
            "detail": str(exc)
        }
    )


async def audio_file_too_large_handler(
    request: Request, exc: AudioFileTooLargeError
) -> JSONResponse:
    logger.warning(f"Audio file too large: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "AudioFileTooLarge",
            "detail": str(exc)
        }
    )


async def transcription_error_handler(
    request: Request, exc: TranscriptionError
) -> JSONResponse:
    logger.error(f"Transcription error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "TranscriptionError",
            "detail": str(exc)
        }
    )


async def structured_extraction_error_handler(
    request: Request, exc: StructuredExtractionError
) -> JSONResponse:
    logger.error(f"Structured extraction error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "StructuredExtractionError",
            "detail": str(exc)
        }
    )


async def voice_recognition_error_handler(
    request: Request, exc: VoiceRecognitionError
) -> JSONResponse:
    logger.error(f"Voice recognition error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "VoiceRecognitionError",
            "detail": str(exc)
        }
    )


async def general_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    logger.exception(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "InternalServerError",
            "detail": f"An unexpected error occurred: {str(exc)}"
        }
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(InvalidAudioFormatError, invalid_audio_format_handler)
    app.add_exception_handler(AudioFileTooLargeError, audio_file_too_large_handler)
    app.add_exception_handler(TranscriptionError, transcription_error_handler)
    app.add_exception_handler(StructuredExtractionError, structured_extraction_error_handler)
    app.add_exception_handler(VoiceRecognitionError, voice_recognition_error_handler)
    
    app.add_exception_handler(Exception, general_exception_handler)
