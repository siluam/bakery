(require [hyrule [-> ->>]])

(defn static/freezer [value freezer]
                      (cond [(not value) (setv freezer [])]
                            [(isinstance value list)
                             (do (if (not (isinstance freezer list)) (setv freezer []))
                                 (.extend freezer value)
                                 (setv freezer (->> (lfor i
                                                          (lfor j freezer :if j j)
                                                          (if (isinstance i list) i [i]))
                                                    (list)
                                                    (chain #*))))]
                            [True (raise (TypeError f"Sorry! The 'm/freezer' can only accept lists or non-truthy values!"))])
  (return freezer))

(print (static/freezer [[1 2] [3 4] 5))