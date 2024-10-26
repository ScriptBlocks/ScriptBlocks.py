import simpleaudio as sa
from pydub import AudioSegment
import io
import wave
import asyncio

class Sound:
    def __init__(self, path):
        self.path = path

    def _convert_to_wav(self):
        # Load the audio file and convert to WAV format using pydub
        audio = AudioSegment.from_file(self.path)
        wav_data = io.BytesIO()
        audio.export(wav_data, format="wav")
        wav_data.seek(0)
        return wav_data

    def play_sync(self):
        try:
            # Convert to WAV
            wav_data = self._convert_to_wav()

            # Read the WAV data into a wave.Wave_read object
            with wave.open(wav_data, 'rb') as wav_file:
                wave_obj = sa.WaveObject.from_wave_read(wav_file)
                play_obj = wave_obj.play()
                play_obj.wait_done()  # Block until the sound is done playing

        except Exception as e:
            print(f"Error during playback: {e}")

    async def play_async(self):
        try:
            # Convert to WAV
            wav_data = self._convert_to_wav()

            # Play asynchronously using an executor
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self._play_wav_async, wav_data)

        except Exception as e:
            print(f"Error during playback: {e}")

    def _play_wav_async(self, wav_data):
        with wave.open(wav_data, 'rb') as wav_file:
            wave_obj = sa.WaveObject.from_wave_read(wav_file)
            play_obj = wave_obj.play()
            play_obj.wait_done()  # Block until the sound is done playing