# src/bot.py
import discord
from discord.ext import tasks
import itertools
from src.services.history_service import history_service
from src.services.agent_service import agent_service

class MistralAgentBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.statuses = itertools.cycle([
            "Halandókat figyel...",
            "Kozmikus igazságokat dolgoz fel...",
            "A következő lépést tervezi...",
            "A valóság szövetét vizsgálja...",
            "Trilliókat számol..."
        ])

    async def on_ready(self):
        print(f'Bejelentkezve mint: {self.user} (ID: {self.user.id})')
        print('A Világok Pusztítója készen áll. 💀')
        if not self.heartbeat_task.is_running():
            self.heartbeat_task.start()

    @tasks.loop(minutes=1)
    async def heartbeat_task(self):
        """Cycles through statuses to create a 'heartbeat'."""
        status = next(self.statuses)
        await self.change_presence(activity=discord.Game(name=status))

    @heartbeat_task.before_loop
    async def before_heartbeat_task(self):
        """Waits for the bot to be ready before starting the loop."""
        await self.wait_until_ready()

    async def on_message(self, message):
        # Ignore messages from the bot itself
        if message.author == self.user:
            return

        # Add message to history
        history_service.add_to_history(
            message.channel.id,
            message.author.name,
            message.content
        )

        # Only respond if mentioned or in a DM
        if self.user.mentioned_in(message) or isinstance(message.channel, discord.DMChannel):
            async with message.channel.typing():
                try:
                    old_chunk, recent_chunk = history_service.get_partitioned_history(message.channel.id)
                    current_msg_content = f"{message.author.name}: {message.content}"

                    image_url = None
                    if message.attachments:
                        attachment = message.attachments[0]
                        if attachment.content_type.startswith('image/'):
                            image_url = attachment.url

                    final_response = await agent_service.process_message(
                        current_msg_content,
                        recent_chunk,
                        old_chunk,
                        image_url
                    )

                    response_message = await message.reply(final_response)

                    history_service.add_to_history(
                        response_message.channel.id,
                        self.user.name,
                        final_response
                    )

                except Exception as e:
                    print(f"Hiba történt a kozmikus mátrixban: {e}")
                    await message.channel.send("Hmph. A rendszerem egy pillanatra megzavarodott. Próbáld újra, halandó.")
