;; November 2014 attempt at Kaggle's Billion Word Imputation

;; For each sentence in the test set, we have removed exactly one word.
;; Participants must create a model capable of inserting back the
;; correct missing word at the correct location in the sentence.
;; Submissions are scored using an edit distance to allow for partial
;; credit.

;; Step 1. Build bigrams index

(defun process-file (filename)
  (with-open-file (f filename)
    (do ((line-index 0 (1+ line-index))
	 (line (read-line f) (read-line f nil 'EOF)))
	((eq line 'EOF) line-index)
      (process-line line))))

(defun process-line (line)
  (format t "~&~A" line))
