import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ImportProgressConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def send_progress(self, progress):
        await self.send(text_data=json.dumps({
            'progress': progress
        }))
