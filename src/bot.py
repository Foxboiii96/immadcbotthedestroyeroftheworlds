import discord
from collections import deque
from src.agents.historian import agent_historian_summarize
from src.agents.strategist import agent_strategist_analyze
from src.agents.responder import agent_responder_generate

class MistralAgentBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel_history = {}
        self.max_history = 50

    async def on_ready(self):
        print(f'Bejelentkezve mint: {self.user} (ID: {self.user.id})')
        print('A 3-ágens rendszer aktív.')

    async def add_to_history(self, message):
        channel_id = message.channel.id
        if channel_id not in self.channel_history:
            self.channel_history[channel_id] = deque(maxlen=self.max_history)

        self.channel_history[channel_id].append(f"{message.author.name}: {message.content}")

    async def on_message(self, message):
        if message.author == self.user:
            await self.add_to_history(message)
            return

        await self.add_to_history(message)

        if self.user.mentioned_in(message) or isinstance(message.channel, discord.DMChannel):
            async with message.channel.typing():
                try:
                    history = list(self.channel_history.get(message.channel.id, []))

                    split_index = max(0, len(history) - 15)
                    old_chunk = history[:split_index]
                    recent_chunk = history[split_index:]

                    summary = await agent_historian_summarize(old_chunk)

                    current_msg_content = f"{message.author.name}: {message.content}"
                    strategy = await agent_strategist_analyze(current_msg_content, summary)

                    final_response = await agent_responder_generate(
                        current_msg_content,
                        recent_chunk,
                        summary,
                        strategy
                    )

                    await message.reply(final_response)

                except Exception as e:
                    print(f"Hiba történt: {e}")
                    await message.channel.send("Sajnálom, hiba történt a feldolgozás során.")
