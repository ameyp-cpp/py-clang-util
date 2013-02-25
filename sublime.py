class Selection:
    def init(self, regions):
        self._regions = regions

    def clear():
        self._regions = []

class Region:
    def init(self, begin, end):
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

class View:
    def init(self, file_name, line_num, col_num):
        self._file = open(file_name, 'r')

        content = self._file.readlines()
        for i in range(1, line_num):
            self._file.readline()

        self._sel = Selection([Region(self._file.tell(), self._file.tell() + col_num - 1)])

    def file_name(self):
        return self._file.name

    def line(position):
        self._file.seek(0)
        content = self._file.read(position)
        beg = content.rfind('\n') + 1
        return Region(beg, position)

    def substr(self, region):
        self._file.seek(region.begin())
        content = self._file.read(region.end() - region.begin())
        return content

    def rowcoll(self, position):
        self._file.seek(0)
        content = self._file.read(position)
        newlines = content.count('\n')

        self._file.seek(0)
        for i in range(1, newlines):
            self._file.readline()

        column = position - self._file.tell()
        return newlines + 1, column + 1

    def is_dirty():
        return False

    def sel(self):
        return self._sel
