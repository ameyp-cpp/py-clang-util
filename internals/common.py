"""
Copyright (c) 2011-2012 Fredrik Ehnbom

This software is provided 'as-is', without any express or implied
warranty. In no event will the authors be held liable for any damages
arising from the use of this software.

Permission is granted to anyone to use this software for any purpose,
including commercial applications, and to alter it and redistribute it
freely, subject to the following restrictions:

   1. The origin of this software must not be misrepresented; you must not
   claim that you wrote the original software. If you use this software
   in a product, an acknowledgment in the product documentation would be
   appreciated but is not required.

   2. Altered source versions must be plainly marked as such, and must not be
   misrepresented as being the original software.

   3. This notice may not be removed or altered from any source
   distribution.
"""

import threading
import time
import Queue
import os
import re
import sys
import traceback

from Pymacs import lisp
import time

class Settings():
    def __init__(self):
        self._dict = {
            "enable": True,
            "automatic_completion_popup": True,
            "worker_threadcount": -1,
            "enable_fast_completions": True,
            "recompile_delay": 0,
            "hide_output_when_empty": False,
            "show_output_panel": False,
            "update_output_panel": True,
            "output_panel_use_syntax_file": False, #delta
            "show_status": True,
            "show_visual_error_marks": True,
            "error_marks_on_panel_only": False,
            "index_parse_options": 13,
            "warm_up_in_separate_thread": True,
            "cache_on_load": True,
            "remove_on_close": True,
            "pop_on_close": True,
            "reparse_on_activated": True,
            "reparse_on_save": True,
            "reparse_use_dirty_buffer": False,
            "parse_status_messages": True,
            "analyzer_status_messages": True,
            "marker_output_panel_scope": "invalid",
            "marker_warning_scope": "comment",
            "marker_error_scope": "invalid",
            "time_completions": False,
            "inhibit_sublime_completions": True,
            "dont_complete_startswith": ["~","operator"],
            "add_language_option": True,
            "additional_language_options": {
                    "c++": [],
                    "c": [],
                    "objc": [],
                    "objc++": []
                },
            "options": [
                "-isystem", "/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.7.sdk/usr/include/",
                "-isystem", "/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.7.sdk/usr/include/c++/4.2.1",
                "-F/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.7.sdk/System/Library/Frameworks/",
                "-Wno-deprecated-declarations",
                "-isystem", "C:\\MinGW\\lib\\gcc\\mingw32\\4.7.0\\include",
                "-isystem", "C:\\MinGW\\lib\\gcc\\mingw32\\4.7.0\\include\\c++",
                "-isystem", "C:\\MinGW\\lib\\gcc\\mingw32\\4.7.0\\include\\c++\\mingw32",
                "-isystem", "C:\\MinGW\\include",
                "-Wall"
                ],
            "options_script": "",
            "dont_prepent_clang_includes": False,
            "debug_options": True,
            "marker_analyzer_output_panel_scope": "invalid",
            "marker_analyzer_scope": "invalid",
            "analyzer_commandline": [
                "clang",
                "--analyze",
                "-o",
                "-"
                ],
            "analyzer_extensions": [
                "cpp",
                "c",
                "cc",
                "m",
                "mm"
                ],
            "diagnostic_ignore_dirs": [
                ],
            "diagnostic_ignore_regex": "pragma once in main file"
        }

    def get(self, key, default):
        if (self._dict.has_key(key)):
            return self._dict[key]

        return default

class EmacsLog:
    def __init__(self,category):
        self.logBuffer="*LogBuffer*" # "*Pymacs Log Buffer*"
        self.category=category
        self.startTime=time.time()

    def show(self,level,msg):
        start = int(time.time()-self.startTime)
        mx = str(start) + " <" + level + "> PY " + self.category + " " + msg
        lisp.message(mx)
        #mx = mx + "\n"
        #lisp.set_buffer(self.logBuffer)
        #lisp.insert(mx)

    def error(self, msg):
        self.show("E", msg)

    def info(self, msg):
        self.show("I", msg)

    def debug(self,msg):
        self.show("DEBUG", msg)

    # Finest debugging
    def debugf(self,msg):
        self.show("DEBUG FINER", msg)

loaded = False
loaded_callbacks = []
emacs_logger = EmacsLog("common")

def get_buffer_as_text(file_name, beg = 0, end = 0):
    f=open(file_name,"r")
    if end != 0 and beg < end:
        f.seek(beg)
        text = f.read(end - beg)
    else:
        text = f.read()
    f.close()
    return text

def write_buffer(file_name, text):
    f=open(file_name,"w")
    f.write(text)
    f.close()
    self.reloadBuffer()

def format_current_file(file_name):
    row, col = get_row_col(get_line_number(), lisp.point())
    return "%s:%d:%d" % (file_name, row, col)

def goto_line(line_num):
    lisp.goto_char(lisp.point_min())
    for i in range(1, int(line_num)):
        lisp.forward_line(i)

def get_line_number():
    return int(lisp.what_line()[5:])

def get_line_till_point(line_num, point):
    goto_line(line_num)
    beg = lisp.point()
    line = get_buffer_as_text(lisp.buffer_file_name(), beg, point)
    lisp.goto_char(point)
    return line

def get_row_col(line_num, point):
    goto_line(line_num)
    col = point - lisp.point()
    lisp.goto_char(point)
    return (line_num, col)

def get_prefix(line_num, point):
    prefix = ""
    word_regex = re.compile("\w")
    line = get_line_till_point(line_num, point)
    if word_regex.match(line[-1]):
        prefix = line[-1]

    return prefix

def open_file(filename):
    arr = filename.split(":")
    file_name, line_num, col_num = arr[0], int(arr[1]), int(arr[2])
    lisp.find_file(filename)
    goto_line(line_num)
    lisp.goto_char(lisp.point() + col_num)

def plugin_loaded():
    global loaded
    global loaded_callbacks
    loaded = True
    for c in loaded_callbacks:
        c()
    loaded_callbacks = []

def are_we_there_yet(x):
    global loaded_callbacks
    if loaded:
        x()
    else:
        loaded_callbacks.append(x)

def run_in_main_thread(func):
    #sublime.set_timeout(func, 0)
    func()
    return

def error_message(msg):
    emacs_logger.error(msg)
    return

def status_message(msg):
    if msg[:4] == "Line":
        fil = open("/home/aparulekar/traceback", 'w')
        traceback.print_stack(file=fil)
        fil.close()
    emacs_logger.info(msg)

def get_language():
    file_name = lisp.buffer_file_name()
    if ( file_name == None ):
        return None

    if ( file_name[-4:] == '.cpp' ):
        return 'c++'
    elif ( file_name[-2:] == '.c' or file_name[-2:] == '.h' ):
        return 'c'
    elif ( file_name[-2:] == '.m' ):
        return 'objc'
    elif ( file_name[-3:] == '.mm' ):
        return 'objc++'

def is_supported_language():
    if not get_setting("enabled", True) or lisp.buffer_file_name() == None:
        return False

    language = get_language()
    if language == None or (language != "c++" and
                            language != "c" and
                            language != "objc" and
                            language != "objc++"):
        return False
    return True

def get_settings():
    return Settings()

def get_setting(key, default=None):
    return get_settings().get(key, default)

def expand_path():
    value = lisp.buffer_file_name()
    return value

def display_user_selection(options, callback):
    sublime.active_window().show_quick_panel(options, callback)

class LockedVariable:
    def __init__(self, var):
        self.var = var
        self.l = threading.Lock()

    def try_lock(self):
        return self.l.acquire(False)

    def lock(self):
        self.l.acquire()
        return self.var

    def unlock(self):
        self.l.release()

class Worker(object):
    def __init__(self, threadcount=-1):
        if threadcount < 1:
            threadcount = get_cpu_count()
        self.tasks = Queue.Queue()
        for i in range(threadcount):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            t.start()

    def display_status(self):
        status_message(self.status)

    def set_status(self, msg):
        self.status = msg
        run_in_main_thread(self.display_status)

    def worker(self):
        try:
            # Just so we give time for the editor itself to start
            # up before we start doing work
            if sys.version[0] != '3':
                time.sleep(5)
        except:
            pass
        while True:
            task, data = self.tasks.get()
            try:
                task(data)
            except:
                import traceback
                traceback.print_exc()
            finally:
                self.tasks.task_done()

def complete_path(value):
    path_init, path_last = os.path.split(value)
    if path_init[:2] == "-I" and (path_last == "**" or path_last == "*"):
        starting_path = path_init[2:]
        include_paths = []
        if os.path.exists(starting_path):
            if path_last == "*":
                for dirname in os.listdir(starting_path):
                    if not dirname.startswith("."):  # skip directories that begin with .
                        include_paths.append("-I" + os.path.join(starting_path, dirname))
            elif path_last == "**":
                for dirpath, dirs, files in os.walk(starting_path):
                    for dirname in list(dirs):
                        if dirname.startswith("."):  # skip directories that begin with .
                            dirs.remove(dirname)
                    if dirpath != starting_path:
                        include_paths.append("-I" + dirpath)
            else:
                include_paths.append("-I" + starting_path)
        else:
            pass  # perhaps put some error here?
        return include_paths
    else:
        return [value]

def get_path_setting(key, default=None):
    value = get_setting(key, default)
    opts = []
    if isinstance(value, list):
        for v in value:
            opts.append(expand_path())
    else:
        opts.append(expand_path())
    return opts

def get_cpu_count():
    cpus = 1
    try:
        import multiprocessing
        cpus = multiprocessing.cpu_count()
    except:
        pass
    return cpus
