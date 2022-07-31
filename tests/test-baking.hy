(import bakery [ls])
(import oreo)
(import oreo [nots?])
(import pathlib [Path])
(require hyrule [->])
(setv cookies (/ (.resolve (. (Path __file__) parent parent) :strict True) "cookies"))
(setv cookies-ls (.ls oreo cookies))
(setv assorted-cookies (.ls oreo cookies :sort True))
(defn test-baking []
      (.bake- ls :a True :m/progress "green" cookies)
      (for [item ls]
           (when (nots? item) (assert (in item cookies-ls)))))
