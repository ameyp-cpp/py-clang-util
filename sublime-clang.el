(defun ac-source-sublime-clang
  '((init . sublime-clang-init)
    (candidates . sublime-clang-completions)))

(defun sublime-clang-init ()
  (pymacs-exec "from SublimeClang import sublimeclang")
  (setq sublime-clang-completer
	(pymacs-eval "sublimeclang.SublimeClangAutoComplete().on_query_completions")))

(defun sublime-clang-completions()
  (setq sublime-clang-completer (sublimeclang-SublimeClangAutoComplete))
  (pymacs-call (pymacs-call "getattr" sublime-clang-completer "on_query_completions") ".")
