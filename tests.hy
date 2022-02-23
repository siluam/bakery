(import richy.traceback)
(.install richy.traceback)

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

#@(zoom (defn list-output []
              (import bakery [ls])
              (-> (ls)
                  (sorted)
                  (= (ls :m/list True :m/sort None))
                  (assert))))

#@(zoom (defn main []
              (import bakery [ls])
              (import os [listdir])
              (-> cookies
                  (ls :m/list True)
                  (.sort)
                  (= (.sort (lfor item (listdir cookies) :if (not (.startswith item ".")) item)))
                  (assert))))

#@(zoom (defn program-options []
              (import bakery [ls])
              (import os [listdir])
              (-> cookies
                  (ls :m/list True :a True)
                  (.sort)
                  (= (.sort (listdir cookies)))
                  (assert))))

#@(zoom (defn context-manager []
              (import bakery [ls])
              (import os [listdir])
              (with [lsa (ls :a True cookies :m/context True :m/list True)]
                    (-> (lsa)
                        (.sort)
                        (= (.sort (listdir cookies)))
                        (assert)))
              (-> cookies
                  (ls :m/list True)
                  (.sort)
                  (= (.sort (lfor item (listdir cookies) :if (not (.startswith item ".")) item)))
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
                  (ls :a True :m/list True)
                  (.sort)
                  (= (.sort (listdir cookies)))
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
              (import os [listdir])
              (setv tails (| (ls [] :a True cookies :m/list True) tail)
                    output (.sort (tails)))
              #_(-> cookies
                  (listdir)

                  ;; TODO: Why does this end at -1? Cut doesn't work like slices
                  (cut 10 -1))

              (assert (= output (.sort (cut (listdir cookies) 10 -1))))))

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
              (setv bulbasaur (.sort [ "001: Bulbasaur" "002: Ivysaur" "003: Venusaur" ])
                    last-three (.sort [ "058: Growlithe" "059: Arcanine" "060: Poliwag" ]))

              (-> cookies
                  (+ "/01")
                  (cat :m/n-lines 3 :m/list True)
                  (.sort)
                  (= bulbasaur)
                  (assert))

              (-> cookies
                  (+ "/01")
                  (cat :m/n-lines (, 3) :m/list True)
                  (.sort)
                  (= bulbasaur)
                  (assert))

              (-> cookies
                  (+ "/01")
                  (cat :m/n-lines { "number" 3 } :m/list True)
                  (.sort)
                  (= bulbasaur)
                  (assert))

              (-> cookies
                  (+ "/01")
                  (cat :m/n-lines (, True 3) :m/list True)
                  (.sort)
                  (= last-three)
                  (assert))

              (-> cookies
                  (+ "/01")
                  (cat :m/n-lines { "last" True "number" 3 } :m/list True)
                  (.sort)
                  (= last-three)
                  (assert))))

(for [func (eclair funcs "tests" "blue")] (func))
