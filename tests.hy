(import rich.traceback)
(.install rich.traceback)

(import alive-progress [alive-it])
(import os [path :as osPath])

(setv funcs [])
(defn zoom [func] (.append funcs func))

(setv cookies (.join osPath (.dirname osPath (.realpath osPath __file__)) "cookies"))

(defn not-dots? [string] (not (or (= string ".") (= string ".."))))

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
              (for [item (ls :a True cookies :m/progress True)]
                   (if (not-dots? item)
                       (assert (in item output))))))

#@(zoom (defn baking []
              (import bakery [ls])
              (import os [listdir])
              (.bake- ls :a True :m/progress True cookies)
              (setv output (listdir cookies))
              (for [item ls]
                   (if (not-dots? item)
                       (assert (in item output))))))

(for [func (alive-it funcs)]
     (func))
