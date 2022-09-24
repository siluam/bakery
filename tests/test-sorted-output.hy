(import bakery [ls])
(import oreo)
(import oreo [nots?])
(import pathlib [Path])
(import pytest [mark])
(require hyrule [->])
(setv cookies (/ (.resolve (. (Path __file__) parent parent) :strict True) "cookies"))
(setv cookies-ls (.ls oreo cookies))
(setv assorted-cookies (.ls oreo cookies :key True))
(import bakery [frosting])
(defn sort-func [item] (if (.isnumeric item) (int item) (ord (get item 0))))
(defn [mark.sorted-output (.parametrize mark "opts" #({ "m/list" True } { "m/type" frosting } { "m/frosting" True }))] test-sorted-output [opts]
      (assert (= assorted-cookies (ls cookies :m/sort None #** opts))))
(defn [mark.sorted-output] test-sorted-key-output []
      (assert (= (.ls oreo cookies :key sort-func) (ls cookies :m/list True :m/sort sort-func))))
(defn [mark.sorted-output] test-sorted-reversed-output [] (assert (= (cut assorted-cookies None None -1) (ls cookies :m/list True :m/sort True))))
(defn [mark.sorted-output] test-sorted-dict-keyword []
      (assert (= (.ls oreo cookies :key sort-func :reverse True) (ls cookies :m/list True :m/sort { "key" sort-func "reverse" True }))))
