(defvar ac-source-sublime-clang
  '((init . py-clang-init)
    (candidates . py-clang-auto-complete)))

(defun py-clang-init ()
  (pymacs-exec "from SublimeClang import sublimeclang")
  (setq sublime-clang-auto-complete
	(pymacs-eval "sublimeclang.SublimeClangAutoComplete()"))
  (setq sublime-clang-completer
	(pymacs-call "getattr" sublime-clang-auto-complete "on_query_completions"))
  (setq sublime-clang-on-post-save
	(pymacs-call "getattr" sublime-clang-auto-complete "on_post_save"))
  (setq sublime-clang-on-modified
	(pymacs-call "getattr" sublime-clang-auto-complete "on_modified"))
  (setq sublime-clang-on-load
	(pymacs-call "getattr" sublime-clang-auto-complete "on_load"))
  (setq sublime-clang-on-close
	(pymacs-call "getattr" sublime-clang-auto-complete "on_close"))
  )

(defun py-clang-auto-complete ()
  (funcall sublime-clang-completer))

(defun py-clang-on-post-save ()
  (funcall sublime-clang-on-post-save))

(defun py-clang-on-modified ()
  (funcall sublime-clang-on-modified))

(defun py-clang-on-load ()
  (funcall sublime-clang-on-load))

(defun py-clang-on-close ()
  (funcall sublime-clang-on-close))

;(add-hook 'after-save-hook 'py-clang-on-post-save)
;(add-hook 'after-change-functions 'py-clang-on-modified)
;(add-hook 'find-file-hook 'py-clang-on-load)
;(add-hook 'kill-buffer-hook 'py-clang-on-close)
