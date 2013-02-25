import sublimeclang
from sublime import View

scaa = sublimeclang.SublimeClangAutoComplete()
completions = []

option = 1

if option == 1:
    flags = [
            "-I/home/aparulekar/Developer/GamePlay/gameplay/src","-I/home/aparulekar/Developer/GamePlay/external-deps/bullet/include","-I/home/aparulekar/Developer/GamePlay/external-deps/oggvorbis/include","-I/home/aparulekar/Developer/GamePlay/external-deps/libpng/include","-I/home/aparulekar/Developer/GamePlay/external-deps/zlib/include","-I/home/aparulekar/Developer/GamePlay/external-deps/lua/include","-I/home/aparulekar/Developer/GamePlay/external-deps/glew/include"
        ]
    view = View("/home/aparulekar/Developer/GamePlay/gameplay-samples/sample00-mesh/src/MeshGame.cpp", 46, 11, flags)
    completions = scaa.on_query_completions(view, "", [1362])
elif option == 2:
    view = View("/home/aparulekar/tmp/test.cpp", 22, 8)
    completions = scaa.on_query_completions(view, "", [433])

print completions
