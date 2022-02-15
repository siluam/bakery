(import rich.traceback)
(.install rich.traceback)

(import alive-progress [alive-it])
(import os [path :as osPath])

(setv funcs [])
(defn zoom [func] (.append funcs func))

(setv cookies (.join osPath (.dirname osPath (.realpath osPath __file__)) "cookies"))

(defn nots? [string] (not (or (= string ".") (= string ".."))))

#@(zoom (defn main []
              (print "Testing Main...")
              (import bakery [ls])
              (import os [listdir])
              (setv output (ls cookies))
              (assert (all (gfor item (listdir cookies) :if (and (not (.startswith item "."))
                                                                   (in item output)) item)))
              (print "Testing Main Complete!")))

#@(zoom (defn program-options []
              (print "Testing Program Options...")
              (import bakery [ls])
              (import os [listdir])
              (setv output (ls :a True cookies))
              (assert (all (gfor item (listdir cookies) :if (in item output) item)))
              (print "Testing Program Options Complete!")))

#@(zoom (defn context-manager []
              (print "Testing Context Manager...")
              (import bakery [ls])
              (import os [listdir])
              (with [lsa (ls :a True cookies :m/context True)]
                    (setv output (lsa))
                    (assert (all (gfor item (listdir cookies) :if (in item output) item))))
              (setv output (ls cookies))
              (assert (all (gfor item (listdir cookies) :if (and (not (.startswith item "."))
                                                                   (in item output)) item)))
              (print "Testing Context Manager Complete!")))

#@(zoom (defn loop []
              (print "Testing Loop...")
              (import bakery [ls])
              (import os [listdir chdir getcwd])
              (setv output (listdir cookies)
                    cwd (getcwd))
              (try (chdir cookies)
                   (for [item ls]
                        (assert (in item output)))
                   (finally (chdir cwd)))
              (print "Testing Loop Complete!")))

#@(zoom (defn progress []
              (print "Testing Progress...")
              (import bakery [ls])
              (import os [listdir])
              (setv output (listdir cookies))
              (for [item (ls :a True cookies :m/progress True)]
                   (if (nots? item)
                       (assert (in item output))))
              (print "Testing Progress Complete!")))

#@(zoom (defn baking []
              (print "Testing Baking...")
              (import bakery [ls])
              (import os [listdir])
              (.bake- ls :a True :m/progress True cookies)
              (setv output (listdir cookies))
              (for [item ls]
                   (if (nots? item)
                       (assert (in item output))))
              (print "Testing Baking Complete!")))

#@(zoom (defn freezing []
              (print "Testing Freezing...")
              (import bakery [ls steakery])
              (assert (isinstance (ls []) steakery))
              (print "Testing Freezing Complete!")))

#@(zoom (defn git-status []
              (print "Testing Git Status...")
              (import bakery [git])
              (assert (= (.status (git :C cookies) :m/str True)
                         "On branch main\nYour branch is up to date with 'origin/main'.\n\nnothing to commit, working tree clean"))
              (print "Testing Git Status Complete!")))

(for [func (alive-it funcs)]
     (func))
