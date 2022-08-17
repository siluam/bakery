(import bakery [ls])
(import oreo)
(import oreo [nots?])
(import pathlib [Path])
(import pytest [mark])
(require hyrule [->])
(setv cookies (/ (.resolve (. (Path __file__) parent parent) :strict True) "cookies"))
(setv cookies-ls (.ls oreo cookies))
(setv assorted-cookies (.ls oreo cookies :key True))
(defn [mark.progress] test-progress []
      (for [item (ls :a True cookies :m/progress "red")]
           (when (nots? item) (assert (in item cookies-ls)))))
