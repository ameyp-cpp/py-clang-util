import sublimeclang
from sublime import View

completions = []

flags = ["-I/home/aparulekar/Developer/GamePlay/gameplay/src","-I/home/aparulekar/Developer/GamePlay/external-deps/bullet/include","-I/home/aparulekar/Developer/GamePlay/external-deps/oggvorbis/include","-I/home/aparulekar/Developer/GamePlay/external-deps/libpng/include","-I/home/aparulekar/Developer/GamePlay/external-deps/zlib/include","-I/home/aparulekar/Developer/GamePlay/external-deps/lua/include","-I/home/aparulekar/Developer/GamePlay/external-deps/glew/include"]
filename = "/home/aparulekar/Developer/GamePlay/gameplay-samples/sample00-mesh/src/MeshGame.cpp"
position = 1300
prefix = ""
view = View(filename, position, flags)
folders = ["/home/aparulekar/Developer/GamePlay"]

def found_completions(completions):
    print completions

scaa = sublimeclang.SublimeClangAutoComplete()
scaa.on_query_completions(view, prefix, [position], found_completions)

def found_definition(target):
    if target == None:
        print "Unable to find target"

    print target

cgb = sublimeclang.SublimeClangGoto()
cgb.goto("definition", view, folders, found_definition)
