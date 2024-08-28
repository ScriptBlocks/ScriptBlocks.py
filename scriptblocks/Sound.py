import asyncio
from ffmpeg import FFmpeg as SyncFFmpeg
from ffmpeg.asyncio import FFmpeg as AsyncFFmpeg

class Sound:
    def __init__(self, path):
        self.path = path
        self.speed = 1.0
        self.pitch = 1.0
        self.volume = 1.0

    def _generate_atempo_filters(self, tempo):
        atempo_filters = []
        if tempo < 0.5:
            while tempo < 0.5:
                atempo_filters.append("atempo=0.5")
                tempo *= 2.0
        elif tempo > 2.0:
            while tempo > 2.0:
                atempo_filters.append("atempo=2.0")
                tempo /= 2.0
        if 0.5 <= tempo <= 2.0:
            atempo_filters.append(f"atempo={tempo}")
        return ', '.join(atempo_filters)

    def _get_audio_params(self):
        tempo = self.speed * self.pitch
        atempo_filter_str = self._generate_atempo_filters(tempo)
        return {
            "format": "wav",
            "ar": "44100",
            "ac": "2",
            "af": f"{atempo_filter_str}, volume={self.volume}"
        }

    def play_sync(self):
        try:
            ffmpeg = SyncFFmpeg()
            ffmpeg.input(self.path)
            ffmpeg.output(
                "pipe:", 
                **self._get_audio_params()
            ).execute()  # Synchronous execution
        except Exception as e:
            print(f"FFmpeg error: {e}")

    async def play_async(self):
        try:
            ffmpeg = AsyncFFmpeg()
            ffmpeg.input(self.path)
            ffmpeg.output(
                "pipe:",
                **self._get_audio_params()
            )
            await ffmpeg.execute()  # Asynchronous execution
        except Exception as e:
            print(f"FFmpeg error: {e}")

