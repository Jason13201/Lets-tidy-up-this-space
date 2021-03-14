import discord
from config import BotToken

intents = discord.Intents(messages=True, guilds=True, members=True)


class MyClient(discord.Client):
    async def on_ready(self):
        print("Logged on as {0}!".format(self.user))

        while True:
            memberTag, taskInfo = discordQ.get()
            for guild in client.guilds:
                async for member in guild.fetch_members():
                    if str(member) == memberTag:
                        await member.send(
                            f"Hey there! A task was added to your to-do list: `{taskInfo}`"
                        )

    async def on_message(self, message):
        print("Message from {0.author}: {0.content}".format(message))


client = MyClient(intents=intents)


def runBot(q):
    global discordQ
    discordQ = q
    client.run(BotToken)