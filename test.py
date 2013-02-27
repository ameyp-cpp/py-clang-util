import sublimeclang
from sublime import View

import socket

completions = []

if socket.gethostname() == "firefly-lin":
    flags = ["-I/home/amey/Developer/GamePlay/gameplay/src","-I/home/amey/Developer/GamePlay/external-deps/bullet/include","-I/home/amey/Developer/GamePlay/external-deps/oggvorbis/include","-I/home/amey/Developer/GamePlay/external-deps/libpng/include","-I/home/amey/Developer/GamePlay/external-deps/zlib/include","-I/home/amey/Developer/GamePlay/external-deps/lua/include","-I/home/amey/Developer/GamePlay/external-deps/glew/include"]
    filename = "/home/amey/Developer/GamePlay/Projects/Genesis/src/GenesisGame.cpp"
else:
    flags = ["-I/home/aparulekar/Developer/GamePlay/gameplay/src","-I/home/aparulekar/Developer/GamePlay/external-deps/bullet/include","-I/home/aparulekar/Developer/GamePlay/external-deps/oggvorbis/include","-I/home/aparulekar/Developer/GamePlay/external-deps/libpng/include","-I/home/aparulekar/Developer/GamePlay/external-deps/zlib/include","-I/home/aparulekar/Developer/GamePlay/external-deps/lua/include","-I/home/aparulekar/Developer/GamePlay/external-deps/glew/include"]
    filename = "/home/aparulekar/Developer/GamePlay/Projects/Genesis/src/GenesisGame.cpp"

position = 1060
prefix = ""
view = View(filename, position, flags)
folders = ["/home/amey/Developer/GamePlay"]

def found_completions(completions):
    print len(completions)

scaa = sublimeclang.SublimeClangAutoComplete()
scaa.on_query_completions(view, prefix, [position], found_completions)

def found_definition(target):
    if target == None:
        print "Unable to find target"

    print target

cgb = sublimeclang.SublimeClangGoto()
cgb.goto("definition", view, folders, found_definition)
