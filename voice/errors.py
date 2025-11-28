class VoiceRecognitionError(Exception):
    """Base exception for voice recognition errors"""
    pass


class InvalidAudioFormatError(VoiceRecognitionError):
    """Raised when audio format is not supported"""
    pass


class AudioFileTooLargeError(VoiceRecognitionError):
    """Raised when audio file exceeds size limit"""
    pass


class TranscriptionError(VoiceRecognitionError):
    """Raised when transcription fails"""
    pass


class StructuredExtractionError(VoiceRecognitionError):
    """Raised when structured data extraction fails"""
    pass
