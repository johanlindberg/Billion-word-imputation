;; November 2014 attempt at Kaggle's Billion Word Imputation

;; For each sentence in the test set, we have removed exactly one word.
;; Participants must create a model capable of inserting back the
;; correct missing word at the correct location in the sentence.
;; Submissions are scored using an edit distance to allow for partial
;; credit.

;; Step 1. Build bigrams index

(use-package :cl-ppcre)

(defparameter *MAX-LINES* 10) 
(defparameter *HEART-BEAT-INTERVAL* 100000)

(defparameter *BIGRAMS* (make-hash-table :test 'equal))

(defparameter *tf* ; training file on SD Card
  "/media/removable/SD Card/Billion-Word-Imputation/train_v2.txt")
(defparameter *to*
  "~/Downloads/Playground/Kaggle/Billion-Word-Imputation/lisp/bigrams.lisp")

(defun process-file (filename store)
  "process-file reads the contents of <filename> and produces lisp code to
   produce the bigrams hash-table which is saved to <store>."
  (with-open-file (out store :direction :output :if-exists :supersede)
    (with-open-file (in filename)
      (do ((line-index 0 (1+ line-index))
	   (line (read-line in) (read-line in nil 'EOF)))
	  ((or (and *MAX-LINES*
		    (>= line-index *MAX-LINES*))
	       (eq line 'EOF))
	   (values *BIGRAMS* line-index))
	(when (eq 0 (mod line-index *HEART-BEAT-INTERVAL*))
	  (format t "."))
	; -- process-line produces a string of lisp code
	(write-line (process-line line) out)))))

(defun process-line (line)
  (let ((words (cl-ppcre:split "\\s+" line))
	(result ""))
    (do ((i 1 (1+ i)))
	((>= i (length words)))
      (let* ((w1 (nth (- i 1) words))
	     (w2 (nth i words))
	     (*print-escape* t))
	(unless (gethash w1 *BIGRAMS*)
	  (setf (gethash w1 *BIGRAMS*) t 
		result
		(format nil "~A~%(setf (gethash ~W *BIGRAMS*) (make-hash-table :test 'equal))" result w1)))
	(setq result
	      (format nil "~A~%(incf (gethash ~W (gethash ~W *BIGRAMS*) 0))" result w2 w1))))
    result))
