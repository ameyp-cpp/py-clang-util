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
    def __init__(self, file_name, line_num, col_num):
        self._file = open(file_name, 'r')

        for i in range(0, line_num):
            self._file.readline()

        self._sel = [Region(self._file.tell(), self._file.tell() + col_num)]
        self._settings = {}

    def file_name(self):
        return self._file.name

    def line(self, position):
        self._file.seek(0)
        content = self._file.read(position)
        beg = content.rfind('\n') + 1
        self._file.readline()
        end = self._file.tell() - 1
        return Region(beg, end)

    def substr(self, region):
        self._file.seek(region.begin())
        content = self._file.read(region.end() - region.begin())
        return content

    def rowcol(self, position):
        self._file.seek(0)
        content = self._file.read(position)
        newlines = content.count('\n')

        self._file.seek(0)
        for i in range(0, newlines):
            self._file.readline()

        column = position - self._file.tell()
        return newlines, column

    def scope_name(self, position):
        # Doesn't do anything
        return "source.c++"

    def is_dirty(self):
        return False

    def is_scratch(self):
        return False

    def sel(self):
        return self._sel

    def settings(self):
        return self._settings

def load_settings(settings_file):
    fd = open(settings_file, 'r')
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
