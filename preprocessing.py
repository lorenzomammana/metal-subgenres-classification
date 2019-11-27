import re
from nltk.corpus import wordnet

# https://www.youtube.com/watch?v=r37OYsdH6Z8


class RepeatReplacer(object):
    def __init__(self):
        self.regex = re.compile(r'(\w*)(\w)\2(\w*)')
        self.repl = r'\1\2\3'

    def replace(self, word):
        loop_res = self.regex.sub(self.repl, word)

        if word == loop_res:
            return loop_res
        else:
            return self.replace(loop_res)

    def replace_with_wordnet(self, word):
        if wordnet.synsets(word):
            return word

        loop_res = self.regex.sub(self.repl, word)

        if word == loop_res:
            return loop_res
        else:
            return self.replace(loop_res)