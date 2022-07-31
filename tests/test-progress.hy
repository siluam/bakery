(import bakery [ls])
(import oreo)
(import oreo [nots?])
(import pathlib [Path])
(require hyrule [->])
(setv cookies (/ (.resolve (. (Path __file__) parent parent) :strict True) "cookies"))
(setv cookies-ls (.ls oreo cookies))
(setv assorted-cookies (.ls oreo cookies :sort True))
(defn test-progress []
      (for [item (ls :a True cookies :m/progress "red")]
           (when (nots? item) (assert (in item cookies-ls)))))
