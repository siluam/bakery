(import rich.traceback)
(.install rich.traceback)

(import oreo [eclair either?])
(import os [path :as osPath])

(setv funcs [])
(defn zoom [func] (.append funcs func))

(setv cookies (.join osPath (.dirname osPath (.realpath osPath __file__)) "cookies"))

(defn nots? [string] (not (or (= string ".") (= string ".."))))

#@(zoom (defn main []
              (import bakery [ls])
              (import os [listdir])
              (setv output (ls cookies))
              (assert (all (gfor item (listdir cookies) :if (and (not (.startswith item "."))
                                                                   (in item output)) item)))))

#@(zoom (defn program-options []
              (import bakery [ls])
              (import os [listdir])
              (setv output (ls :a True cookies))
              (assert (all (gfor item (listdir cookies) :if (in item output) item)))))

#@(zoom (defn context-manager []
              (import bakery [ls])
              (import os [listdir])
              (with [lsa (ls :a True cookies :m/context True)]
                    (setv output (lsa))
                    (assert (all (gfor item (listdir cookies) :if (in item output) item))))
              (setv output (ls cookies))
              (assert (all (gfor item (listdir cookies) :if (and (not (.startswith item "."))
                                                                   (in item output)) item)))))

#@(zoom (defn loop []
              (import bakery [ls])
              (import os [listdir chdir getcwd])
              (setv output (listdir cookies)
                    cwd (getcwd))
              (try (chdir cookies)
                   (for [item ls]
                        (assert (in item output)))
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
              (setv ls (bakery :program- "ls")
                    output (ls :a True cookies))
              (assert (all (gfor item (listdir cookies) :if (in item output) item)))))

#@(zoom (defn freezing []
              (import bakery)
              (import bakery [ls])
              (assert (either? (ls []) bakery))))

#@(zoom (defn git-status []
              (import bakery [git])
              (assert (= (.status (git :C cookies) :m/str True)
                         "On branch main\nYour branch is up to date with 'origin/main'.\n\nnothing to commit, working tree clean"))))

#@(zoom (defn string-output []
              (import bakery [echo])
              (assert (= (echo :m/str True "Hello!") "Hello!"))))

#@(zoom (defn piping/first []
              (import bakery [ls tail])
              (import os [listdir])
              (setv tails (| (ls [] :a True cookies) tail)
                    output (tails))
              (assert (all (gfor item (cut (listdir cookies) 10 -1) :if (in item output) item)))))

#@(zoom (defn piping/both []
              (import bakery [env grep])
              (setv egrep (| (env [] :m/exports { "FOO" "bar" } :m/str True) (grep [] "FOO")))
              (assert (= (egrep) "FOO=bar"))))

#@(zoom (defn exports []
              (import bakery [echo])
              (assert (= (echo :m/exports { "FOO" "bar" } "$FOO" :m/str True) "bar"))))

(for [func (eclair funcs "tests" "blue")] (func))
