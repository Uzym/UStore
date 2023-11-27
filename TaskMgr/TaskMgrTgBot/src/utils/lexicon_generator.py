from emoji import emojize


class Lexicon:
    prefix: str = ""
    title: str = "Неизвестно"
    suffix: str = ""

    def __str__(self):
        return self.prefix + self.title + self.suffix

    def __init__(self, title: str, prefix: str = "", suffix: str = ""):
        self.title = title
        self.prefix = prefix
        self.suffix = suffix

    def __call__(self, *args, **kwargs):
        return self.__str__()


class ActionLexicon(Lexicon):
    def __init__(self, title: str, parent_lexicon: Lexicon, full_title: str = None):
        super().__init__(title=title)
        self.parent_lexicon = parent_lexicon
        self.full_title = full_title

    def __str__(self):
        if self.full_title is None:
            return (self.prefix + self.parent_lexicon.prefix +
                    self.title + emojize(" ") + self.parent_lexicon.title +
                    self.suffix + self.parent_lexicon.suffix)
        return self.full_title


class EntityLexicon(Lexicon):
    def __init__(self, title: str, one: str = None, many: str = None,
                 update: str = None, create: str = None, delete: str = None):
        super().__init__(title=title)
        self.update = ActionLexicon(emojize(":pencil:Изменить"), self, update)
        self.create = ActionLexicon(emojize(":droplet:Создать"), self, create)
        self.delete = ActionLexicon(emojize(":fire:Удалить"), self, delete)
        self.one = Lexicon(title if one is None else one)
        self.many = Lexicon(title if many is None else many)
