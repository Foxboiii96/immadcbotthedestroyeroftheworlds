# src/bot.py
import discord
from src.services.history_service import history_service
from src.services.agent_service import agent_service

class MistralAgentBot(discord.Client):
    async def on_ready(self):
        print(f'Bejelentkezve mint: {self.user} (ID: {self.user.id})')
        print('A Világok Pusztítója készen áll. 💀')

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
                    # Get partitioned history from the service
                    old_chunk, recent_chunk = history_service.get_partitioned_history(message.channel.id)

                    current_msg_content = f"{message.author.name}: {message.content}"

                    # Delegate processing to the agent service
                    final_response = await agent_service.process_message(
                        current_msg_content,
                        recent_chunk,
                        old_chunk
                    )

                    response_message = await message.reply(final_response)

                    # Add the bot's own response to the history
                    history_service.add_to_history(
                        response_message.channel.id,
                        self.user.name,
                        final_response
                    )

                except Exception as e:
                    print(f"Hiba történt a kozmikus mátrixban: {e}")
                    await message.channel.send("Hmph. A rendszerem egy pillanatra megzavarodott. Próbáld újra, halandó.")
