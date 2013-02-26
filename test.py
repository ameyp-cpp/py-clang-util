import sublimeclang
from sublime import View

scaa = sublimeclang.SublimeClangAutoComplete()
completions = []

flags = [
            "-I/home/aparulekar/Developer/GamePlay/gameplay/src","-I/home/aparulekar/Developer/GamePlay/external-deps/bullet/include","-I/home/aparulekar/Developer/GamePlay/external-deps/oggvorbis/include","-I/home/aparulekar/Developer/GamePlay/external-deps/libpng/include","-I/home/aparulekar/Developer/GamePlay/external-deps/zlib/include","-I/home/aparulekar/Developer/GamePlay/external-deps/lua/include","-I/home/aparulekar/Developer/GamePlay/external-deps/glew/include"
        ]
filename = "/home/aparulekar/Developer/GamePlay/gameplay-samples/sample00-mesh/src/MeshGame.cpp"
position = 1362
prefix = ""
view = View(filename, position, flags)
print scaa.on_query_completions(view, prefix, view.position)

view = View(filename, position + 1, flags)
prefix = "s"
scaa.reparse(view)
print scaa.on_query_completions(view, prefix, view.position)
