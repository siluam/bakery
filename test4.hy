(defmacro printer [#* chain] `(print ~chain))
(printer '(ls :l True :a True))
