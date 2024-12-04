import ollama

from utils.textbook import TextbookPrompt



class Engine:
    def __init__(self):
        self.ollama = ollama()

    def get_response(self,prompt:TextbookPrompt):
        return self