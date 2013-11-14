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
try:
    import Queue
except:
    import queue as Queue
import os
import re
import sys

if sys.version[0] == '2':
    def sencode(s):
        return s.encode("utf-8")

    def sdecode(s):
        return s

    def bencode(s):
        return s
    def bdecode(s):
        return s
else:
    def sencode(s):
        return s

    def sdecode(s):
        return s

    def bencode(s):
        return s.encode("utf-8")

    def bdecode(s):
        return s.decode("utf-8")

loaded = False
loaded_callbacks = []
def plugin_loaded():
    global loaded
    global loaded_callbacks
    loaded = True
    for c in loaded_callbacks:
        c()
    loaded_callbacks = []

try:
    import sublime
except ImportError:
    from .. import sublime

def are_we_there_yet(x):
    global loaded_callbacks
    if loaded:
        x()
    else:
        loaded_callbacks.append(x)

def run_in_main_thread(func, args=()):
    #sublime.set_timeout(func, 0)
    print args
    func(*args)

def error_message(msg):
    # Work around for http://www.sublimetext.com/forum/viewtopic.php?f=3&t=9825
    sublime.error_message(msg)

language_regex = re.compile("(?<=source\.)[\w+#]+")


def get_language(view):
    caret = view.sel()[0].a
    language = language_regex.search(view.scope_name(caret))
    if language == None:
        return None
    return language.group(0)


def is_supported_language(view):
    if view.is_scratch() or not get_setting("enabled", True, view) or view.file_name() == None:
        return False
    language = get_language(view)
    if language == None or (language != "c++" and
                            language != "c" and
                            language != "objc" and
                            language != "objc++"):
        return False
    return True

def status_message(msg):
    # sublime.status_message(sdecode(msg))
    print(sdecode(msg))

def get_settings():
    module_path = os.path.abspath(__file__)
    root_dir = os.path.dirname(os.path.dirname(module_path))
    return sublime.load_settings(os.path.join(root_dir, "SublimeClang.sublime-settings"))

def get_setting(key, default=None, view=None):
    try:
        if view == None:
            view = sublime.active_window().active_view()
        s = view.settings()
        if s.has("sublimeclang_%s" % key):
            return s.get("sublimeclang_%s" % key)
    except:
        pass
    return get_settings().get(key, default)

def display_user_selection(options, callback):
    sublime.active_window().show_quick_panel(options, callback)

"""
except:
    # Just used for unittesting
    def are_we_there_yet(f):
        f()

    def error_message(msg):
        raise Exception(msg)

    def get_setting(key, default=None, view=None):
        return default

    def get_language(view):
        return "c++"

    def run_in_main_thread(func):
        func()

    def status_message(msg):
        print(msg)

    def display_user_selection(options, callback):
        callback(0)
"""

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

def get_path_setting(key, default=None, view=None):
    value = get_setting(key, default, view)
    opts = []
    if isinstance(value, list):
        for v in value:
            opts.append(v)
    else:
        opts.append(value)
    return opts

def get_cpu_count():
    cpus = 1
    try:
        import multiprocessing
        cpus = multiprocessing.cpu_count()
    except:
        pass
    return cpus
