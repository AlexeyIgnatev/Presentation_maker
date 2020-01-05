import wikipedia
from wikipedia.exceptions import DisambiguationError, PageError

exclude = ['== См. также ==',
           '== Ссылки ==',
           '== Примечания ==',
           '== Источники ==',
           '== Литература ==',
           '== See also ==',
           '== Notes ==',
           '== References ==',
           '== Further reading ==',
           '== External links ==']


class Wiki:
    def __init__(self):
        self.page = None
        self.content = ''
        self.topic = ''

    def load_page(self, topic):
        topic = topic.title()
        try:
            self.page = wikipedia.page(topic)
        except DisambiguationError:
            return 1
        except PageError:
            return 2
        self.content = self.page.content
        self.topic = topic

    def clean_page(self):
        content = self.content.split('\n')
        self.content = '= {} =\n'.format(self.topic)
        prev = False
        for i in content:
            if i in exclude:
                break
            if prev:
                prev = False
                if i == '':
                    continue
            if i.startswith('=='):
                prev = True
                self.content += '\n'
            self.content += i
            if i != '':
                self.content += '\n'
        self.content = self.content.strip()

        # Очистка последних заголовков
        while self.content.split('\n')[-1].startswith('=='):
            self.content = '\n'.join(self.content.split('\n')[:-1]).strip()

    @property
    def headers(self):
        headers = []
        content = self._get_equals()
        for i in content:
            s = i.replace('=', '').strip()
            headers.append(s)
        return headers

    @staticmethod
    def set_lang(lang):
        wikipedia.set_lang(lang)

    def _get_equals(self):
        content = self.content.split('\n')
        content = [i for i in content if i.startswith('==')]
        return content
