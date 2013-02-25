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
    def __init__(self, file_name, position, flags=[], is_dirty=False, content=""):
        self._file = open(file_name, 'rU')

        self._sel = [Region(position, position)]
        self._settings = Settings({"sublimeclang_options": flags})
        self._is_dirty = is_dirty

        if self._is_dirty:
            self._content = content
        else:
            self._content = ""

    def file_name(self):
        return self._file.name

    def line(self, position):
        content = ""
        beg, end = 0, 0

        if not self.is_dirty():
            self._file.seek(0)
            content = self._file.read(position)
            beg = content.rfind('\n') + 1
            self._file.readline()
            end = self._file.tell() - 1
        else:
            content = self._content[:position].rfind('\n') + 1
            end = self._content.find('\n', beg)

        return Region(beg, end)

    def substr(self, region):
        content = ""

        if not self.is_dirty():
            self._file.seek(region.begin())
            content = self._file.read(region.end() - region.begin())
        else:
            content = self._content[region.begin():region.end()]

        return content

    def rowcol(self, position):
        newlines, column = 0, 0

        if not self.is_dirty():
            self._file.seek(0)
            content = self._file.read(position)
            newlines = content.count('\n')

            self._file.seek(0)
            for i in range(0, newlines):
                self._file.readline()
            column = position - self._file.tell()
        else:
            newlines = self._content[:position].count('\n')
            beg_of_line = -1
            for i in range(0, newlines):
                beg_of_line = self._content[:position].find('\n', beg_of_line + 1)
            column = position - beg_of_line

        return newlines, column

    def size(self):
        length = 0

        if not self.is_dirty():
            self._file.seek(0)
            content = self._file.read()
            length = len(content)
        else:
            length = len(self._content)

        return length

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
        position = [self.sel()[0].begin()]

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
