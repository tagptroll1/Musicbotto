from collections import deque


class Controller:
    def __init__(
        self,
        bot,
        voice_client,
        guild,
        owner
    ):
        self.voice_client = voice_client
        self.owner = owner
        self.guild = guild
        self.playlist = deque()

    def add_song(self, entry):
        pass
