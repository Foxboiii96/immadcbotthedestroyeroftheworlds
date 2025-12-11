# src/bot.py
import discord
from discord.ext import tasks
from src.services.history_service import history_service
from src.services.agent_service import agent_service
from src.agents.consciousness import agent_consciousness_generate_thought

class MistralAgentBot(discord.Client):
    async def on_ready(self):
        print(f'Bejelentkezve mint: {self.user} (ID: {self.user.id})')
        print('A Világok Pusztítója készen áll. 💀')
        if not self.heartbeat_task.is_running():
            self.heartbeat_task.start()

    @tasks.loop(minutes=1)
    async def heartbeat_task(self):
        """Generates a thought from the consciousness agent and sets it as status."""
        try:
            thought = await agent_consciousness_generate_thought()
            await self.change_presence(activity=discord.Game(name=thought))
        except Exception as e:
            print(f"Hiba a szívverés során: {e}")
            # Fallback status in case of an error
            await self.change_presence(activity=discord.Game(name="A kozmoszt kémleli..."))

    @heartbeat_task.before_loop
    async def before_heartbeat_task(self):
        """Waits for the bot to be ready before starting the loop."""
        await self.wait_until_ready()

    async def on_message(self, message):
        if message.author == self.user:
            return

        history_service.add_to_history(
            message.channel.id,
            message.author.name,
            message.content
        )

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
                    await message.channel.send("Jaj, valami fura energia van a rendszerben! ✨ Bocsii, próbáld újra légyszi! 💖")
