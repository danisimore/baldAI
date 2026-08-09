from uuid import uuid4
from pathlib import Path
from faster_whisper import WhisperModel
from aiogram.types import Message

TMP_DIR = Path("tmp")
"""A directory for temporary storage of voice message files."""

TMP_DIR.mkdir(exist_ok=True)


class Transcriber:
    """Voice message transcriber."""

    def __init__(self):
        self.model = WhisperModel("small", device="cpu", compute_type="int8")

    async def download_voice(self, message: Message) -> Path:
        """Downloads the voice message received from the user.

        Args:
            message (Message): message received from the user.

        Returns:
            Path: The path to the saved voice message file.
        """
        voice = message.voice
        assert voice is not None

        file = await message.bot.get_file(voice.file_id)

        destination = TMP_DIR / f"{uuid4()}.ogg"

        await message.bot.download(file=file, destination=destination)

        return destination

    def transcribe(self, path: str) -> str:
        """Transcribes the voice message file.

        Args:
            path (str): File path.

        Returns:
            str: The text obtained as a result of transcription.
        """
        segments, _ = self.model.transcribe(
            path,
            language="ru",
            vad_filter=True,
        )

        return "".join(segment.text for segment in segments).strip()
