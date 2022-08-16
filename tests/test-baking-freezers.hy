(import bakery [ls])
(import oreo)
(import oreo [nots?])
(import pathlib [Path])
(import pytest [mark])
(require hyrule [->])
(setv cookies (/ (.resolve (. (Path __file__) parent parent) :strict True) "cookies"))
(setv cookies-ls (.ls oreo cookies))
(setv assorted-cookies (.ls oreo cookies :sort True))
(import bakery [tail])
(import hy [mangle eval] oreo [first-last-n])
(setv tails (| (ls [] :a True cookies) tail))
(defn [mark.baking mark.piping (.parametrize mark "fhash" #(tails.m/freezer-hash (hash (tuple tails.m/freezer))))] test-bake-freezer [fhash]
      (try (.bake- ls :freezer-hash fhash :m/list True :m/sort None :m/filter nots?)
           (-> assorted-cookies (first-last-n :last True :number 10 :type- list) (= (tails)) assert)
           (-> (ls) (isinstance list) (not) assert)
           (finally (.splat- ls :freezer-hash fhash)
                    (assert (not (in (mangle "m/sort") (get tails.m/kwargs.freezer fhash)))))))
(defn [mark.baking mark.piping (.parametrize mark "cls" #(
      {}
      { "base_program" "tail" }
      { "program" "tail" }
))] test-bake-freezer-failures [cls]
      (let [ command (tails :m/return-command True) ]
           (try (.bake- tails cookies :m/list True :help True #** cls)
                (assert (= command (tails :m/return-command True)))
                (finally (.splat- tails #** cls)
                         (-> tails.m/kwargs.baked (get tails.m/subcommand.default) (get (mangle "m/type")) (!= list) assert)))))
