import random

import discord

from commands.command import Command


class Pendu(Command):

    letters = ["a",'à','â','b','c','d','e','é','è','ê','f','g','h','i','j','k','l','m','n','o','ô','p','q','r','s','t','u','û','v','w','x','y','z']

    ascii_arts = [
        '=========',
        '''
                |
                |
                |
                |
                |
        =========
        ''',
        '''
            +---+
            |   |
                |
                |
                |
                |
        =========
        ''',
        '''
            +---+
            |   |
            O   |
                |
                |
                |
        =========
        ''',
        '''
            +---+
            |   |
            O   |
            |   |
                |
                |
        =========
        ''',
        '''
            +---+
            |   |
            O   |
            |\  |
                |
                |
        =========
        ''',
        '''
            +---+
            |   |
            O   |
           /|\  |
                |
                |
        =========
        ''',
        '''
            +---+
            |   |
            O   |
           /|\  |
                |
                |
        =========
        ''',
        '''
            +---+
            |   |
            O   |
           /|\  |
           / \  |
                |
        =========
        ''',
        '''
            +---+
            |   |
            O   |
          ----- |     
           /|\  |
           / \  |
                |
        =========
        '''
    ]

    def __init__(self):
        super().__init__(
            name="Pendu",
            description="Joue au pendu",
            author="Vincent W"
        )
        self.wrong_guesses_limit = len(self.ascii_arts)


    async def execute(self, message: discord.Message, client: discord.Client):
        words = open("assets/francais.txt", "r")
        word = random.choice(words.readlines()).lower().strip()
        guessed_word = ''.join(('■' if l in self.letters else l) for l in word)

        wrong_guesses = 0

        channel = message.channel

        used_letters = []

        await channel.send(f"Bienvenu au pendu. Vous (les cons) devez deviner le mot en {self.wrong_guesses_limit} essais, bonne chance")
        await channel.send(self.build_message(guessed_word, wrong_guesses, used_letters))

        def check(msg):
            return msg.channel.id == channel.id and not msg.content in used_letters and not msg.author == client.user

        while word != guessed_word and wrong_guesses < self.wrong_guesses_limit:
            
            try: 
                message = await client.wait_for('message', check=check, timeout=30.0)
            except:
                await channel.send("Vous avez pris trop de temps pour jouer, c'est fini les fdp")
                return

            content = message.content.lower().strip()

            if len(content) > 1:
                if word == content:
                    await channel.send(f"Bravo {message.author.mention}, fils de con, t'as trouvé le mot: **{word}** (pas si dur que ça en vrai)")
                    return
                else:
                    wrong_guesses += 1
            else:
                found_letter = False
                used_letters.append(content)

                for [i, l] in enumerate(word):
                    if l == content:
                        guessed_word = guessed_word[:i] + l + guessed_word[i+1:]
                        found_letter = True

                if not found_letter: wrong_guesses += 1  

            await channel.send(self.build_message(guessed_word, wrong_guesses, used_letters))          

        if word == guessed_word:
            await channel.send(f"Bravo {message.author.mention}, fils de con, t'as trouvé le mot: **{word}** (pas si dur que ça en vrai)")
        else:
            await channel.send(f"Tu n'as pas trouvé le mot: **{word}**, t'es vraiment une merde")
        return


    def build_message(self, guessed_word, guesses, used_letters):
        return f''' ```\n {self.ascii_arts[guesses]}\n MOT: {guessed_word}\n LETTRES: {'-'.join(used_letters)}```
                '''
