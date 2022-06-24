# pip install chatterbot==1.0.4
# https://ai.recodeminds.com/news/building-an-ai-based-chatbot-in-python/
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer # Custom input data
from chatterbot.trainers import ChatterBotCorpusTrainer #data provided by Chatterbot

# Initiates the bot object
freshBot = ChatBot(
    name="freshBot",
    logic_adapters = ["chatterbot.logic.BestMatch"],                 
    storage_adapter = "chatterbot.storage.SQLStorageAdapter"
)

# Sets bot to train on Chatterbot corpus data
corpus_trainer = ChatterBotCorpusTrainer(freshBot)
corpus_trainer.train("chatterbot.corpus.english")

# sets chatbot to train on custom data
#ListTrainer(freshBot).train("<list>")

while True:
    user_input = input()
    if user_input == 'quit':
        break
    print(freshBot.get_response(user_input))