import discord


def send_message(user_id, message):
    # Créer le client Discord
    client = discord.Client(intents=discord.Intents.default())

    # Fonction pour envoyer un message à un utilisateur
    async def envoyer_message_utilisateur(user_id, message):
        user = await client.fetch_user(user_id)
        print(user)
        await user.send(message)

    # Fonction appelée lorsque le bot est prêt
    @client.event
    async def on_ready():
        print('Bot prêt')
        await envoyer_message_utilisateur(user_id, message)
        await client.close()

    # Démarrer le bot
    client.run('MTEwMDM2MTgyNTQ0MDIzOTY3Ng.GAqJHi.20GKlr5s3l-7i5EptodBcOUs8V1wb6z5VwtASY')


# send_message(1077331451500052612,"test")
