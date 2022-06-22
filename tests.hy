(import rich.traceback)
(.install rich.traceback)

(import oreo [eclair either? nots?])
(import os [path :as osPath])

(require hyrule [->])

(setv funcs [])
(defn zoom [func] (.append funcs func))

(setv cookies (.join osPath (.dirname osPath (.realpath osPath __file__)) "cookies"))

#@(zoom (defn list-output []
              (import bakery [ls])
              (-> cookies
                  (ls :m/list True)
                  (isinstance list)
                  (assert))
              (-> cookies
                  (ls :m/type list)
                  (isinstance list)
                  (assert))))

#@(zoom (defn sorted-output []
              (import bakery [ls])
              (-> (ls)
                  (sorted)
                  (= (ls :m/list True :m/sort None))
                  (assert))))

#@(zoom (defn filtered-output []
              (import bakery [ls])
              (setv sixteen [ "11" "12" "13" "14" "15" "16" ])
              (-> cookies
                  (ls :m/list True :m/filter (fn [item] (and (.isnumeric item) (not (in "0" item)))))
                  (= sixteen)
                  (assert))
              (-> cookies
                  (ls :m/list True :m/filter (, True (fn [item] (or (not (.isnumeric item)) (in "0" item)))))
                  (= sixteen)
                  (assert))))

#@(zoom (defn main []
              (import bakery [ls])
              (import os [listdir])
              (assert (= (ls :m/list True cookies :m/sort None :m/filter (, True (fn [item] (.startswith item "."))))
                         (sorted (gfor item (listdir cookies) :if (not (.startswith item ".")) item))))))

#@(zoom (defn program-options []
              (import bakery [ls])
              (import os [listdir])
              (-> cookies
                  (listdir)
                  (sorted)
                  (= (ls :m/list True :a True cookies :m/sort None :m/filter nots?))
                  (assert))))

#@(zoom (defn context-manager []
              (import bakery [ls])
              (import os [listdir])
              (with [lsa (ls :a True cookies :m/context True :m/list True :m/sort None :m/filter nots?)]
                    (-> cookies
                        (listdir)
                        (sorted)
                        (= (lsa))
                        (assert)))
              (-> cookies
                  (ls :m/list True :m/sort None :m/filter (, True (fn [item] (.startswith item "."))))
                  (= (sorted (gfor item (listdir cookies) :if (not (.startswith item ".")) item)))
                  (assert))))

#@(zoom (defn loop []
              (import bakery [ls])
              (import os [listdir chdir getcwd])
              (setv output (listdir cookies)
                    cwd (getcwd))
              (try (chdir cookies)
                   (for [item ls] (assert (in item output)))
                   (finally (chdir cwd)))))

#@(zoom (defn progress []
              (import bakery [ls])
              (import os [listdir])
              (setv output (listdir cookies))
              (for [item (ls :a True cookies :m/progress "red")]
                   (if (nots? item)
                       (assert (in item output))))))

#@(zoom (defn baking []
              (import bakery [ls])
              (import os [listdir])
              (.bake- ls :a True :m/progress "green" cookies)
              (setv output (listdir cookies))
              (for [item ls]
                   (if (nots? item)
                       (assert (in item output))))))

#@(zoom (defn module-call []
              (import bakery)
              (import os [listdir])
              (setv ls (bakery :program- "ls"))
              (-> cookies
                  (listdir)
                  (sorted)
                  (= (ls :a True :m/list True :m/sort None :m/filter nots? cookies))
                  (assert))))

#@(zoom (defn freezing []
              (import bakery)
              (import bakery [ls])
              (-> []
                  (ls)
                  (either? bakery)
                  (assert))))

#@(zoom (defn git-status []
              (import bakery [git])
              (-> (git :C cookies)
                  (.remote :m/str True)
                  (= "origin")
                  (assert))))

#@(zoom (defn string-output []
              (import bakery [echo])
              (-> "Hello!"
                  (echo :m/str True)
                  (= "Hello!")
                  (assert))))

#@(zoom (defn piping/first []
              (import bakery [ls tail])
              (import oreo [first-last-n])
              (import os [listdir])
              (setv tails (| (ls [] :a True cookies :m/list True :m/sort None :m/filter nots? :m/shell "xonsh") tail))
              (-> cookies
                  (listdir)
                  (sorted)
                  (first-last-n :last True :number 10 :type- list)
                  (= (tails))
                  (assert))))

#@(zoom (defn piping/both []
              (import bakery [env grep])
              (setv egrep (| (env [] :m/exports { "FOO" "bar" } :m/str True) (grep [] "FOO")))
              (assert (= (egrep) "FOO=bar"))))

#@(zoom (defn exports []
              (import bakery [echo])
              (-> "$FOO"
                  (echo :m/exports { "FOO" "bar" } :m/str True)
                  (= "bar")
                  (assert))))

#@(zoom (defn trim []
              (import bakery [cat])
              (setv bulbasaur (sorted (, "001: Bulbasaur" "002: Ivysaur" "003: Venusaur" ))
                    last-three (sorted (, "058: Growlithe" "059: Arcanine" "060: Poliwag" )))
              (.bake- cat :m/list True :m/sort None)

              (print (cat (+ cookies "/01") :m/n-lines 3))

              (-> cookies
                  (+ "/01")
                  (cat :m/n-lines 3)
                  (= bulbasaur)
                  (assert))

              (-> cookies
                  (+ "/01")
                  (cat :m/n-lines (, 3))
                  (= bulbasaur)
                  (assert))

              (-> cookies
                  (+ "/01")
                  (cat :m/n-lines { "number" 3 })
                  (= bulbasaur)
                  (assert))

              (-> cookies
                  (+ "/01")
                  (cat :m/n-lines (, True 3))
                  (= last-three)
                  (assert))

              (-> cookies
                  (+ "/01")
                  (cat :m/n-lines { "last" True "number" 3 })
                  (= last-three)
                  (assert))))

#@(zoom (defn splits []
              (import bakery [ls])
              (setv six-two ["6" "5" "4" "3" "2" "09" "08" "07" "06" "05" "04" "03" "02" "00" "0" "0"])
              (-> cookies
                  (ls :m/list True :m/split 1 :m/sort True :m/filter (fn [item] (.isnumeric item)))
                  (= six-two)
                  (assert))))

#@(zoom (defn false-error []
              (import bakery [ls])
              (-> (ls :j True :m/false-error True)
                  (not)
                  (assert))))

(for [func (eclair funcs "tests" "blue")] (func))
