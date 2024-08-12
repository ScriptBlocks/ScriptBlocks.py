import ffmpeg

class Sound:
  def __init__(self, path):
    self.speed = 1
    self.pitch = 1
    self.volume = 1
    self.path = path

  def play(self):
    process = (
        ffmpeg
        .input(self.path)
        .output("pipe:", format="s16le", ar="44100", ac="2")
        .run_async(pipe_stdout=True)
    )
    
    # Read the output from the pipe (which plays the audio)
    process.communicate()