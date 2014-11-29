;; November 2014 attempt at Kaggle's Billion Word Imputation

;; For each sentence in the test set, we have removed exactly one word.
;; Participants must create a model capable of inserting back the
;; correct missing word at the correct location in the sentence.
;; Submissions are scored using an edit distance to allow for partial
;; credit.

;; Step 1. Build bigrams index

(use-package :cl-ppcre)

(defparameter *MAX-LINES* 100000) 
(defparameter *HEART-BEAT-INTERVAL* 50000)

(defvar *BIGRAMS* (make-hash-table :test 'equal))

(defun process-file (filename)
  (with-open-file (f filename)
    (do ((line-index 0 (1+ line-index))
	 (line (read-line f) (read-line f nil 'EOF)))
	((or (and *MAX-LINES*
		  (>= line-index *MAX-LINES*))
	     (eq line 'EOF))
	 (values *BIGRAMS* line-index))
      (when (eq 0 (mod line-index *HEART-BEAT-INTERVAL*))
	(format t "."))
      (process-line line))))

(defun process-line (line)
  (let ((words (cl-ppcre:split "\\s+" line)))
    (mapcar #'(lambda (w1 w2)
		(let ((w1-bigrams (gethash w1 *BIGRAMS*)))
		  (when (null w1-bigrams)
		    (setf  w1-bigrams (make-hash-table :test 'equal)
			  (gethash w1 *BIGRAMS*) w1-bigrams))
		  (incf (gethash w2 w1-bigrams 0))))
	    words (cdr words))))
