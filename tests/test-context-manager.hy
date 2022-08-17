(import bakery [ls])
(import oreo)
(import oreo [nots?])
(import pathlib [Path])
(import pytest [mark])
(require hyrule [->])
(setv cookies (/ (.resolve (. (Path __file__) parent parent) :strict True) "cookies"))
(setv cookies-ls (.ls oreo cookies))
(setv assorted-cookies (.ls oreo cookies :key True))
(import oreo [hidden?])
(defn [mark.context-manager] test-context-manager []
      (with [lsa (ls :a True cookies :m/context True :m/list True :m/sort None :m/filter nots?)]
            (-> assorted-cookies (= (lsa)) assert))
      (-> cookies
          (ls :m/list True :m/sort None :m/filter #(True hidden?))
          (= assorted-cookies)
          assert))
