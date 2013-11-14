import sublimeclang
from sublime import View

import threading
import socket

completions = []

flags = ["-Isrc_ne","-Isrc_ne/h","-Isrc_ne/component","-Isrc_ne/lm","-Isrc_ne/mcm","-I/opt/QNX632/target/qnx6/usr/include/","-I/opt/QNX632/target/qnx6/usr/include/**","-DVARIANT_g","-DFD_SETSIZE=512","-DVARIANT_a","-DQNX","-DQNX_ppc","-D__LITTLEENDIAN__","-D__QNXNTO__","-D__GNUC__=3","-D__PPC__","-D_STD_BEGIN=namespace,std,{","-D_C_STD_BEGIN=namespace,std,{","-D_STD_END=}","-D_C_STD_END=}","_XOPEN_SOURCE-0","-Wno-logical-op-parentheses","-Wno-bitwise-op-parentheses","-Wno-parentheses","-Wno-dangling-else","-Wno-missing-declarations","-Wno-null-conversion"]
filename = "/home/aparulekar/dawn_v1/main/src_ne/component/TH/TransactionHandler.cpp"
folders = ["/home/aparulekar/dawn_v1/main/"]

position = 2139
prefix = ""
view = View(filename, position, flags)
recompile_sem = threading.Semaphore(0)

def print_log(msg):
    print(msg)

def recompile_done():
    sublimeclang.display_compilation_results(view, print_log)
    print "Getting completions."
    scaa.on_query_completions(view, prefix, [position])
    recompile_sem.release()

scaa = sublimeclang.SublimeClangAutoComplete()
print "Recompiling"
scaa.recompile(view, recompile_done)
recompile_sem.acquire(True)

def found_definition(target):
    if target == None:
        print "Unable to find target"

    print ("Target = " + str(target))

cgb = sublimeclang.SublimeClangGoto()
cgb.goto("definition", view, folders, found_definition)
