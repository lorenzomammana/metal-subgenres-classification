import re

givenpatterns = [(r"won't", "will not"),
                 (r"'s", ""),
                 (r"'d", "would"),
                 (r"don't", "not")]


class RegexpReplacer(object):
    def __init__(self):
        self.patterns = givenpatterns

    def replace(self, text):
        for (raw, rep) in self.patterns:
            regex = re.compile(raw)
            text = regex.sub(rep, text)


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