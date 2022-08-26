(import bakery [ls])
(import oreo)
(import oreo [nots?])
(import pathlib [Path])
(import pytest [mark])
(require hyrule [->])
(setv cookies (/ (.resolve (. (Path __file__) parent parent) :strict True) "cookies"))
(setv cookies-ls (.ls oreo cookies))
(setv assorted-cookies (.ls oreo cookies :key True))
(import bakery [tail])
(import hy [mangle eval] oreo [first-last-n])
(setv tails (| (ls [] :a True cookies) tail))
(defn [mark.baking mark.piping (.parametrize mark "fhash" #(tails.m/freezer-hash (hash (tuple tails.m/freezer))))] test-bake-freezer [fhash]
      (try (.bake- ls :freezer-hash- fhash :m/list True :m/sort None :m/filter nots?)
           (-> assorted-cookies (first-last-n :last True :number 10 :type- list) (= (tails)) assert)
           (-> (ls) (isinstance list) not assert)
           (finally (.splat- ls :freezer-hash- fhash)
                    (assert (not (in (mangle "m/sort") (get tails.m/kwargs.freezer fhash)))))))
(defn [mark.baking mark.piping] test-bake-freezer-no-args-non-attr-kwargs []
      (try (.bake- tails cookies :help True :m/list True :m/sort None :m/filter nots?)
           (-> assorted-cookies (first-last-n :last True :number 10 :type- list) (= (tails)) assert)
           (finally (.splat- tails)
                    (assert (not (in (mangle "m/sort") (get tails.m/kwargs.baked tails.m/subcommand.default)))))))
(defn [mark.baking mark.piping (.parametrize mark "opts, cls" #(
      #({ "base_programs_" True } "base_program")
      #({ "base_program_" "ls" } "base_program")
      #({ "programs_" True } "program")
      #({ "program_" "ls" } "program")
      #({ "freezers_" True } "freezer")
      #({ "freezer_hash_" tails.m/freezer-hash } "freezer")
      #({ "freezer_hash_" (hash (tuple tails.m/freezer)) } "freezer")
))] test-piping-macro-baking [opts cls]
    (try (.bake- tails cookies :help True :m/list True :m/sort None :m/filter nots? #** opts)
         (-> assorted-cookies (first-last-n :last True :number 10 :type- list) (= (tails)) assert)
         (finally (.splat- tails #** opts)
                  (let [ k (next (iter (.keys opts)))
                         v (next (iter (.values opts))) ]
                       (assert (not (in (mangle "m/sort") (get (get tails.m/kwargs cls) (cond (= k "freezers_") tails.m/freezer-hash
                                                                                              (isinstance v bool) (getattr tails (mangle (+ "m/" cls)))
                                                                                              True v)))))))))
(defn [mark.baking mark.piping (.parametrize mark "opts, cls" #(
      #({ "base_program_" "tail" } "base_program")
      #({ "program_" "tail" } "program")
))] test-bake-freezer-failures [opts cls]
      (try (.bake- tails cookies :help True :m/list True :m/sort None :m/filter nots? #** opts)
           (-> assorted-cookies (first-last-n :last True :number 10 :type- list) (= (tails)) not assert)
           (finally (.splat- tails #** opts)
                    (assert (not (in (mangle "m/sort") (get (get tails.m/kwargs cls) (next (iter (.values opts))))))))))