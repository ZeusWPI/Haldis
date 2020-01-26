;;;;;:;;;;;;;;;;;;;;;;;;;
;;; Haldis menu files ;;;
;;;;;;;;;;;;;;;;;;;;;;;;;

(defun my-font-lock-restart ()
  "Reload the syntax highlighting"
  (interactive)
  (setq font-lock-mode-major-mode nil)
  (font-lock-fontify-buffer)
  (message "hldsmode: Reloaded syntax highlighting!"))

(defun my-restart-hlds-mode ()
  (interactive)
  (let ((lisp-mode-hook nil))
    (normal-mode)
    (message "hldsmode: Reloaded mode!")))

(setq hlds-font-lock-keywords
      (let* (
             ;; define several category of keywords
             (x-keywords '())
             (x-types '("dish"))
             (x-constants '())
             (x-events '())
             (x-functions '("single_choice" "multi_choice"))

             ;; generate regex string for each category of keywords
             (x-keywords-regexp (regexp-opt x-keywords 'words))
             (x-types-regexp (regexp-opt x-types 'words))
             (x-constants-regexp (regexp-opt x-constants 'words))
             (x-events-regexp (regexp-opt x-events 'words))
             (x-functions-regexp (regexp-opt x-functions 'words))

             ;(x-functions-regexp-final (concat "<h1>\\|</h1>" "\\|" x-functions-regexp))
             (x-constants-regexp-final (concat "\\({[^{]+?}\\)" "\\|" x-constants-regexp))
             (x-keywords-regexp-final (concat "\\(€.+\\)$" "\\|" x-keywords-regexp))
             (x-events-regexp-final (concat "^\\([a-zA-Z0-9_]+?\\):" "\\|" x-events-regexp)))

          `(
            (,x-types-regexp . font-lock-type-face)
            ;(,x-constants-regexp-final . font-lock-constant-face)
            (,x-constants-regexp-final .(1 font-lock-constant-face))
            (,x-events-regexp-final . (1 font-lock-builtin-face))
            (,x-functions-regexp . font-lock-function-name-face)
            (,x-keywords-regexp-final . (1 font-lock-keyword-face))
            ;; note: order above matters, because once colored, that part won't change.
            ;; in general, put longer words first
          )))

(defvar hlds-mode-syntax-table nil "Syntax table for `hlds-mode'.")

(setq hlds-mode-syntax-table
      (let ( (synTable (make-syntax-table)))
        ;; hlds style comment: “== …”
        (modify-syntax-entry ?# "<" synTable)
        (modify-syntax-entry ?\n ">" synTable)
        synTable))

;;;###autoload
(define-derived-mode hlds-mode fundamental-mode "hlds"
  "Major mode for editing Haldis menu files."

  ;; code for syntax highlighting
  (setq font-lock-defaults '((hlds-font-lock-keywords)))

  (set-syntax-table hlds-mode-syntax-table)
  )



;; add the mode to the `features' list
(provide 'hlds-mode)
