import json
import re

class Selection:
    def __init__(self, region):
        self._region = region

class Region:
    def __init__(self, begin, end):
        self._begin = begin
        self._end = end

    def begin(self):
        return self.a

    def end(self):
        return self.b

    @property
    def a(self):
        return self._begin

    @property
    def b(self):
        return self._end

class Settings:
    def __init__(self, settings):
        self._settings = settings

    def has(self, name):
        if name in self._settings.keys():
            return True

        return False

    def get(self, name, default=None):
        if self.has(name):
            return self._settings[name]

        return default

class View:
    def __init__(self, file_name, position, flags=[], tmp_file=None):
        if tmp_file == None:
            self._is_dirty = False
            fil = open(file_name, 'rU')
        else:
            self._is_dirty = True
            fil = open(tmp_file, 'rU')

        self._content = fil.read()
        fil.close()
        self._file_name = file_name
        self._sel = [Region(position, position)]
        self._settings = Settings({"sublimeclang_options": flags})

    def file_name(self):
        return self._file_name

    def line(self, position):
        content = ""
        beg, end = 0, 0

        beg = self._content[:position].rfind('\n') + 1
        end = self._content.find('\n', beg)

        return Region(beg, end)

    def substr(self, region):
        content = self._content[region.begin():region.end()]
        return content

    def rowcol(self, position):
        newlines = self._content[:position].count('\n')
        beg = -1
        for i in range(0, newlines):
            beg = self._content[:position].find('\n', beg + 1)
        column = position - beg - 1

        return newlines, column

    def size(self):
        return(len(self._content))

    def scope_name(self, position):
        # Doesn't do anything
        return "source.c++"

    def is_dirty(self):
        return self._is_dirty

    def is_scratch(self):
        return False

    def sel(self):
        return self._sel

    def settings(self):
        return self._settings

    @property
    def position(self):
        return [self.sel()[0].begin()]

def load_settings(settings_file):
    fd = open(settings_file, 'rU')
    content = fd.read()

    # strip comments
    comment_re = re.compile(
        '(^)?[^\S\n]*/(?:\*(.*?)\*/[^\S\n]*|/[^\n]*)($)?',
        re.DOTALL | re.MULTILINE)
    match = comment_re.search(content)
    while match:
        content = content[:match.start()] + content[match.end():]
        match = comment_re.search(content)

    return Settings(json.loads(content))

def error_message(msg):
    print msg
