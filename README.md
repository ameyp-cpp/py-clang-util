## Description

This is a python module that can be used for a variety of C++-related utility functions, such as code completion with a cache and navigation.
It's a direct port of the [SublimeClang plugin](https://github.com/quarnster/SublimeClang) for the Sublime Text 2 editor, and most of the credit goes to that plugin's author.

## Limitations

I don't know if this works on Windows, and I'm not going to try to get it to work. I've had no luck compiling the 3.2 release of llvm+clang on Windows, and quite frankly I'm not going to bother. If you have any luck fixing the module to work perfectly on Windows, please send me a pull request.

## Features

1. Get code completion candidates at a position in a file.
The results are cached, making subsequent lookups in the same file faster. [Working]
2. Go to definition/implementation of symbol at a position in a file [Working]
3. Go to parent reference of word at a position in a file [Pending]
4. Get a list of compilation errors in a file [Pending]

Line and column numbers and cursor position all start at 0 for the purpose of creating the View object.

## Installation

1. Get the repo with `git clone https://github.com/ameyp/py-clang-util.git --recursive`
2. Only on linux,
  1. cd src
  2. mkdir build
  3. cd build
  4. cmake ..
  5. make
3. Add the repo's path to your PYTHONPATH.

## Usage
```python
    import sublimeclang
    from sublime import View

    # CPP Flags to be passed to clang for compilation.
    flags = ["-I/home/user/project/include", "-D__DEBUG__"]

    # For code completion
    # Create the View object contains information about the file to be parsed.

    view = View("/home/user/project/src/main.cpp", # file's path
                42, # position in file where completion is desired
                flags) # CPP flags

    # Prefix that triggered auto-completion. Blank string for member/static completions,
    # alphanumeric string for variable-name completions.
    # For example, some_object-> would have prefix "", while some_object->s would have prefix "s"
    prefix = ""

    ## First example, auto-complete

    auto_completer = sublimeclang.SublimeClangAutoComplete()

    # Function to be called execution is finished.
    def found_completions(completions):
        # completions is a list of strings, or an empty list if no completions were found.
        print completions

    auto_completer.on_query_completions(view, prefix, view.position, found_completions)

    # List of folders to search in for definition/implementation
    folders = ["/home/user/project"]


    ## Second example, jump to definition/implementation

    # Updated view with cursor at a different position, preferably on a symbol
    view = View("/home/user/project/src/main.cpp", # file's path
                256, # position in file where symbol is located
                flags) # CPP flags

    # Function to be called once execution is finished.
    # Will be one of
    # 1. None if no results were found.
    # 2. A single string if only one result was found.
    # 3. A list of strings if multiple results were found.
    #
    # Each result will be in the format "filepath:line:column"
    def found(target):
        if target == None:
            print "Unable to find target"
        else:
            print target

    # Create the goto object
    cgb = sublimeclang.SublimeClangGoto()

    # The first argument should be "definition" or "implementation"
    cgb.goto("definition", view, folders, found)

```
The completions object returned is a list of all possible completions. Each item in the list is a tuple.
The first element of the tuple is the completion's (i.e. the corresponding reference's) declaration, in the form `Declaration\tReturn-type`.
Subsequent elements are the first element split with function arguments when the corresponding reference is a function declaration, and non-existent for variable declarations.