(import rich.traceback)
(.install rich.traceback :show-locals True)

(import builtins)
(import weakref)

(import addict [Dict :as D])
(import ast [literal-eval])
(import autoslot [Slots SlotsMeta])
(import collections [OrderedDict])
(import copy [copy deepcopy])
(import functools [partial wraps])
(import hy [mangle unmangle])
(import hyrule [coll? inc])
(import inspect [isclass :as class?])
(import itertools [chain tee islice])
(import more-itertools [peekable])
(import oreo [eclair flatten get-un-mangled int? recursive-unmangle tea trim])
(import os [environ path :as osPath getcwd])
(import rich [print inspect])
(import rich.pretty [pretty-repr pprint])
(import rich.progress [Progress])
(import shlex [join split])
(import shutil [which])
(import subprocess [DEVNULL PIPE Popen STDOUT])
(import textwrap [TextWrapper])
(import types [MethodType])

(try (import coconut *)
     (except [ImportError] None))

(try (import cytoolz [first])
     (except [ImportError]
             (import toolz [first])))

(require hyrule [-> ->> assoc])

(defn split-and-flatten [iterable] (flatten (gfor j (flatten iterable) (.split j))))

(defn check [self program] (-> program
                          (which)
                          (is None)
                          (if None self)
                          (return)))

(defclass frosting [tea Slots]

(defn __init__ [self output [capture "stdout"]]
      (setv self.capture (if (= capture "stderr") "stderr" "stdout")
            self.dict-like (isinstance output dict)
            self.iterable (coll? output)
            self.output output)

(cond [self.dict-like (.__init__ (super) #** self.output)]
      [self.iterable (.__init__ (super) #* self.output)]
      [True (.__init__ (super) self.output)])

)

(defn __iter__ [self]
      (yield-from (if self.dict-like
                      (get self self.capture)
                      (.values self))))

(defn __call__ [self]
      (return (cond [(not self.iterable) self.output]
                    [self.dict-like (D (.items self))]
                    [True (.values self)])))

)

(defclass melcery [SlotsMeta]

(defn __init__ [cls #* args #** kwargs] (setv cls.m/stores [])))

(defclass milcery [:metaclass melcery]

(setv __slots__ [ "__weakref__" ])

#@(classmethod (defn cls/freezer [cls value freezer]
                      (cond [(not value) (setv freezer [])]
                            [(coll? value)
                             (do (if (not (isinstance freezer list)) (setv freezer []))
                                 (.extend freezer value)
                                 (setv freezer (flatten (gfor i freezer :if i i))))]
                            [True (raise (TypeError f"Sorry! The 'm/freezer' can only accept non-string iterables or non-truthy values!"))])
                      (return freezer)))

#@(classmethod (defn cls/string-prefix [cls b a] (+ a b)))

#@(classmethod (defn cls/process-attr [cls attr prefix]
                     (setv attr (unmangle attr))
                     (if (.startswith attr prefix)
                         (.replace attr "_" "-")
                         (mangle (.replace (.cls/string-prefix cls (.lstrip attr "_") prefix) "_" "-")))))

#@(classmethod (defn cls/is-attr [cls attr]
                     (setv attr (unmangle attr))
                     (cond [(.endswith attr "__") (return "__")]
                           [(.startswith attr "__") (return "internal/")]
                           [(.startswith attr "_") (return "m/")]
                           [(.startswith attr "internal/") (return "internal/")]
                           [(.startswith attr "m/") (return "m/")]
                           [True (return False)])))

#@(classmethod (defn cls/process-if-attr [cls attr [return-bool False]]
                     (setv attr (unmangle attr))
                     (return (if (setx prefix (.cls/is-attr cls attr))
                                 (mangle (.cls/process-attr cls attr prefix))
                                 (if return-bool False (mangle attr))))))

#@(classmethod (defn cls/remove-if-not-attr [cls dct] (return (dfor [key value] (.items dct) :if (.cls/is-attr cls key) [ key value ]))))

#@(classmethod (defn cls/trim-attr-prefix [cls attr]
                     (setv attr (unmangle attr))
                     (let [prefix (.cls/is-attr cls attr)]
                          (return (, prefix (if prefix (mangle (.removeprefix attr prefix)) (mangle attr)))))))

#@(classmethod (defn cls/get-attr [cls dct attr [default False]]
                     (setv attr (unmangle attr))
                     (setv [prefix cls/get-attr/attr] (.cls/trim-attr-prefix cls attr))
                     (return (or (.get dct (mangle (+ "__" cls/get-attr/attr)) False)
                                 (.get dct (mangle (+ "_" cls/get-attr/attr)) False)
                                 (.get dct (mangle (+ "internal/" cls/get-attr/attr)) False)
                                 (.get dct (mangle (+ "m/" cls/get-attr/attr)) default)))))

#@(property (defn m/freezer [self] (return self.internal/freezer)))
#@(m/freezer.setter (defn m/freezer [self value] (setv self.internal/freezer (.cls/freezer self.__class__ value self.internal/freezer))))

#@(property (defn m/return-command [self] (return self.internal/return-command)))
#@(m/return-command.setter (defn m/return-command [self value]
                                 (setv self.internal/return-command (bool value))
                                 (if value (setv self.m/type str))))

#@(property (defn m/print-command [self] (return self.internal/print-command)))
#@(m/print-command.setter (defn m/print-command [self value]
                                (setv self.internal/print-command (bool value))
                                (if value (setv self.m/return-command True))))

#@(property (defn m/run [self] (return (= self.m/capture "run"))))
#@(m/run.setter (defn m/run [self value] (if value (setv self.m/capture "run"))))

#@(property (defn m/trim [self] (return self.internal/trim)))
#@(m/trim.setter (defn m/trim [self value]
    (setv dict-like (isinstance value dict)
          iterator (coll? value)
          last-default False
          number-default 0
          std-default "stdout"
          std (cond [dict-like (.get value "std" std-default)]
                    [iterator (get (or (lfor item value :if (isinstance item str) item) (, std-default)) 0)]
                    [(isinstance value str) value]
                    [True std-default])
          self.internal/trim (D {

"last" (cond [dict-like (.get value "last" last-default)]
             [iterator (get (or (lfor item value :if (isinstance item bool) item) (, last-default)) 0)]
             [(isinstance value bool) value]
             [True last-default])
"number" (cond [dict-like (.get value "number" number-default)]
               [iterator (get (or (lfor item value :if (int? item) item) (, number-default)) 0)]
               [(int? value) value]
               [True number-default])

"std" (if std
                (if (not (in std (setx stds (, "stdout" "stderr" "both"))))
                    (raise (TypeError #[f[Sorry! You must choose an `std' value from: {(.join ", " stds)}]f]))
                    std))
}))))

#@(property (defn m/c [self] (return self.m/context)))
#@(m/c.setter (defn m/c [self value] (setv self.m/context (bool value))))

#@(property (defn m/capture [self] (return self.internal/capture)))
#@(m/capture.setter (defn m/capture [self value]
                          (if (not (in value self.m/captures))
                              (raise (TypeError #[f[Sorry! Capture type "{value}" is not permitted! Choose from one of: {(.join ", " self.m/captures)}]f])))
                          (setv self.internal/capture value)))

#@(property (defn m/sudo [self] (return self.internal/sudo)))
#@(m/sudo.setter (defn m/sudo [self value]
                       (setv error-message
                             #[[Sorry! `m/sudo' must be a string of "i" or "s", or a dict-like object of length 1, key "i" or "s", and value `user', or a boolean!]]
                             self.internal/sudo (if value
                                                    (if (or (isinstance value bool) (= (len value) 1))
                                                        (cond [(isinstance value str)
                                                               (if (in value (, "i" "s"))
                                                                   { value "root" }
                                                                   (raise (ValueError error-message)))]
                                                              [(isinstance value bool) value]
                                                              [(isinstance value dict) (if (-> value (.keys) (iter) (next) (in (, "i" "s")))
                                                                                                                   value
                                                                                                                   (raise (ValueError error-message)))])
                                                        (raise (ValueError error-message)))
                                                    False))))

#@(property (defn m/exports [self] (return self.internal/exports)))
#@(m/exports.setter (defn m/exports [self value]
                          (setv self.internal/exports value)
                          (if value (setv self.m/intact-command (bool value)))))

#@(property (defn m/new-exports [self] (return self.internal/new-exports)))
#@(m/new-exports.setter (defn m/new-exports [self value]
                              (setv self.internal/new-exports value)
                              (if value (setv self.m/intact-command (bool value)))))

(defn __init__ [
        self
        #* args
        [program- None]
        [base-program- None]
        [freezer- None]
        #** kwargs]

(.append self.__class__.m/stores (.ref weakref self self))

(setv self.m/type-groups (D {}))

(setv self.m/type-groups.acceptable-args [str int])

(setv self.m/type-groups.reprs (, "str" "repr"))

(setv self.m/type-groups.this-class-subclass [self.__class__])
(.extend self.m/type-groups.acceptable-args self.m/type-groups.this-class-subclass)

(setv self.m/type-groups.genstrings [tea])
(.extend self.m/type-groups.acceptable-args self.m/type-groups.genstrings)
(setv self.m/type-groups.genstrings (tuple self.m/type-groups.genstrings))

(setv self.m/type-groups.excluded-classes (, "type"))

(setv self.m/subcommand (D {})
      self.m/subcommand.default "supercalifragilisticexpialidocious"
      self.m/subcommand.current (D {})
      self.m/subcommand.current.unprocessed "supercalifragilisticexpialidocious"
      self.m/subcommand.current.intact False
      self.m/subcommand.current.processed "supercalifragilisticexpialidocious")

(setv self.m/args (D {})
      self.m/args.world []
      self.m/args.instantiated (list args)
      self.m/args.baked (D {})
      self.m/args.baked.supercalifragilisticexpialidocious []
      self.m/args.called []
      self.m/args.current (D {})
      self.m/args.current.unprocessed (D {})
      self.m/args.current.unprocessed.starter []
      self.m/args.current.unprocessed.regular []
      self.m/args.current.processed (D {})
      self.m/args.current.unprocessed.starter []
      self.m/args.current.unprocessed.regular [])

(setv self.m/kwargs (D {})
      self.m/kwargs.world (D {})
      self.m/kwargs.instantiated (D kwargs)
      self.m/kwargs.baked (D {})
      self.m/kwargs.baked.supercalifragilisticexpialidocious (D {})
      self.m/kwargs.called (D {})
      self.m/kwargs.current (D {})
      self.m/kwargs.current.unprocessed (D {})
      self.m/kwargs.current.unprocessed.starter (D {})
      self.m/kwargs.current.unprocessed.regular (D {})
      self.m/kwargs.current.processed (D {})
      self.m/kwargs.current.processed.starter []
      self.m/kwargs.current.processed.regular []
      self.m/kwargs.current.processed.starter-values []
      self.m/kwargs.current.processed.regular-values [])

(setv self.internal/freezer (.cls/freezer self.__class__ freezer- []))

(if program-
    (do (setv self.m/program (or (.replace (unmangle program-) "_" "-") ""))
        (if (in "--" self.m/program)
            (setv self.m/program (.join osPath (getcwd) (.replace self.m/program "--" "."))))
        (if (not (check self self.m/program))
            (raise (ImportError f"cannot import name '{self.m/program}' from '{self.__class__.__module__}'")))
        (setv self.m/base-program (or base-program- self.m/program)))
    (setv self.m/program ""
          self.m/base-program (or base-program- self.m/program)))

(setv self.m/return-categories (,
    "stdout"
    "stderr"
    "return-codes"
    "command"
    "tea"
    "verbosity"
))

(setv self.m/command (tea))

(setv self.m/gitea (D {})
      self.m/gitea.list [ "git" "yadm" ]
      self.m/gitea.bool (or (in self.m/base-program self.m/gitea.list) False)
      self.m/gitea.off False)

(setv self.m/settings (D {})
      self.m/settings.defaults (D {})
      self.m/settings.current (D {}))

(setv self.m/intact-command (bool self.m/freezer))
(setv self.m/settings.defaults.m/intact-command (deepcopy self.m/intact-command))

(setv self.m/settings.programs (D {})
      self.m/current-settings (D {})
      self.m/current-settings.program (D {})
      self.m/current-settings.subcommand (D {}))

(setv self.m/settings.programs.zpool (D {}))

(setv self.m/settings.programs.zpool.import (D { "m/sudo" True }))

(setv self.m/settings.programs.zfs (D {}))

(setv self.m/settings.programs.zfs.load-key (D { "m/run" True
                                                 "m/sudo" True }))

(setv self.m/settings.programs.rich (D {}))

(setv self.m/settings.programs.rich.supercalifragilisticexpialidocious.m/run True)

(setv self.internal/exports (D {}))
(setv self.m/settings.defaults.m/exports (deepcopy self.internal/exports))

(setv self.internal/new-exports (D {}))
(setv self.m/settings.defaults.m/new-exports (deepcopy self.internal/new-exports))

(setv self.m/frozen False)
(setv self.m/settings.defaults.m/frozen (deepcopy self.m/frozen))

(setv self.m/captures (, "stdout" "stderr" "both" "run"))
(setv self.internal/capture "stdout")
(setv self.m/settings.defaults.m/capture (deepcopy self.internal/capture))

(setv self.m/shell None)
(setv self.m/settings.defaults.m/shell (deepcopy self.m/shell))

(setv self.m/dazzle False)
(setv self.m/settings.defaults.m/dazzle (deepcopy self.m/dazzle))

(setv self.m/ignore-stdout False)
(setv self.m/settings.defaults.m/ignore-stdout (deepcopy self.m/ignore-stdout))

(setv self.m/ignore-stderr False)
(setv self.m/settings.defaults.m/ignore-stderr (deepcopy self.m/ignore-stderr))

(setv self.m/stdout-stderr False)
(setv self.m/settings.defaults.m/stdout-stderr (deepcopy self.m/stdout-stderr))

(setv self.m/verbosity 0)
(setv self.m/settings.defaults.m/verbosity (deepcopy self.m/verbosity))

(setv self.m/run-as "")
(setv self.m/settings.defaults.m/run-as (deepcopy self.m/run-as))

(setv self.internal/trim (D { "last" "False" "number" 0 "std" "stdout" }))
(setv self.m/settings.defaults.m/trim (deepcopy self.internal/trim))

(setv self.m/one-dash False)
(setv self.m/settings.defaults.m/one-dash (deepcopy self.m/one-dash))

(setv self.m/fixed False)
(setv self.m/settings.defaults.m/fixed (deepcopy self.m/fixed))

(setv self.m/intact-option False)
(setv self.m/settings.defaults.m/intact-option (deepcopy self.m/intact-option))

(setv self.m/tiered False)
(setv self.m/settings.defaults.m/tiered (deepcopy self.m/tiered))

(setv self.m/input None)
(setv self.m/settings.defaults.m/input (deepcopy self.m/input))

(setv self.m/regular-args (,))
(setv self.m/settings.defaults.m/regular-args (deepcopy self.m/regular-args))

(setv self.m/regular-kwargs (D {}))
(setv self.m/settings.defaults.m/regular-kwargs (deepcopy self.m/regular-kwargs))

(setv self.m/context False)
(setv self.m/settings.defaults.m/context (deepcopy self.m/context))

(setv self.internal/return-command False)
(setv self.m/settings.defaults.m/return-command (deepcopy self.internal/return-command))

(setv self.internal/print-command False)
(setv self.m/settings.defaults.m/print-command (deepcopy self.internal/print-command))

(setv self.m/print-command-and-run False)
(setv self.m/settings.defaults.m/print-command-and-run (deepcopy self.m/print-command-and-run))

(setv self.m/type iter)
(setv self.m/settings.defaults.m/type (deepcopy self.m/type))

(setv self.m/progress None)
(setv self.m/settings.defaults.m/progress (deepcopy self.m/progress))

(setv self.m/split False)
(setv self.m/settings.defaults.m/split (deepcopy self.m/split))

(setv self.m/dos False)
(setv self.m/settings.defaults.m/dos (deepcopy self.m/dos))

(setv self.m/wait True)
(setv self.m/settings.defaults.m/wait (deepcopy self.m/wait))

(setv self.m/popen (D {}))
(setv self.m/settings.defaults.m/popen (deepcopy self.m/popen))

(setv self.internal/sudo False)
(setv self.m/settings.defaults.m/sudo (deepcopy self.internal/sudo))

(setv self.m/debug False)
(setv self.m/settings.defaults.m/debug (deepcopy self.m/debug))
(setv self.m/default-inspect-kwargs (D { "all" True }))
(setv self.m/settings.defaults.m/default-inspect-kwargs (deepcopy self.m/default-inspect-kwargs))

)

(defn misc/type-name-is-string [self [type/type None]]
      (return (in (. (or type/type self.m/type) __name__) self.m/type-groups.reprs)))

(defn m/reset-all [self]
      (.reset- self)
      (.command/reset self))

(defn m/convert-type [self input [type/type None]]
      (if input
          (do (setv type/type/type (or type/type self.m/type))
              (if (isinstance input self.m/type-groups.genstrings)
                  (let [frosted-input (input)]
                       (cond [(isinstance frosted-input str)
                              (setv input [(.fill (TextWrapper :break-long-words False :break-on-hyphens False) frosted-input)])]
                             [(isinstance frosted-input int) (if (.misc/type-name-is-string self :type/type type/type/type)
                                                                 (return (pretty-repr frosted-input))
                                                                 (return frosted-input))])))
              (return (cond [(and self.m/progress (coll? input)) (eclair input (.m/command self) self.m/progress)]
                            [(.misc/type-name-is-string self :type/type type/type/type) (.join "\n" input)]
                            [True (type/type/type input)])))
          (return input)))

(defn subcommand/get [self #** kwargs]
      (setv self.m/subcommand.current.intact (.cls/get-attr self.__class__ kwargs "m/intact-subcommand"))
      (setv subcommand (.cls/get-attr self.__class__ kwargs "m/subcommand" :default self.m/subcommand.default))
      (if (!= subcommand self.m/subcommand.default)
          (setv self.m/subcommand.current.unprocessed subcommand)))

(defn subcommand/process [self]
    (setv self.m/subcommand.current.processed (if self.m/subcommand.current.intact
                                                  self.m/subcommand.current.unprocessed
                                                  (.replace (unmangle self.m/subcommand.current.unprocessed) "_" "-"))))

(defn var/set-defaults [self]
      (for [[key value] (.items self.m/settings.defaults)]
           (setattr self key (deepcopy value)))
      (setv self.m/current-settings.program (get-un-mangled self.m/settings.programs
                                                            self.m/base-program
                                                            :default (D {})))
      (for [[key value] (.items self.m/current-settings.program.supercalifragilisticexpialidocious)]
           (setattr self key (deepcopy value))))

(defn var/setup [self #* args [subcommand- "supercalifragilisticexpialidocious"] #** kwargs]
      (.var/set-defaults self)

      (setv self.m/args.world (or (. (.origin- self) m/args world) []))
      (setv self.m/kwargs.world (or (. (.origin- self) m/kwargs world) (D {})))

      (if (= subcommand- self.m/subcommand.default)
          (do (.subcommand/get self #** self.m/kwargs.world)
              (.subcommand/get self #** self.m/kwargs.instantiated)
              (.subcommand/get self #** (. self m/kwargs baked [subcommand-]))
              (.subcommand/get self #** kwargs))
          (setv self.m/subcommand.current.unprocessed subcommand-))
      (if (not self.m/subcommand.current.unprocessed) (setv self.m/subcommand.current.unprocessed self.m/subcommand.default))
      (.subcommand/process self)

      (setv self.m/current-settings.subcommand (get-un-mangled self.m/current-settings.program
                                                               self.m/subcommand.current.processed
                                                               :default (D {})))
      (for [[key value] (.items self.m/current-settings.subcommand)]
           (setattr self key (deepcopy value)))

      (setv self.m/args.called args)
      (setv self.m/kwargs.called kwargs)

      (.var/process-all self #* args #** kwargs)

      (.var/apply self))

(defn reset- [
            self
            [world False]
            [instantiated False]
            [baked False]
            [args False]
            [kwargs False]
            [all-subs False]
            [subcommand "supercalifragilisticexpialidocious"]
            [set-defaults True]]
      (setv self.m/current-settings (D {}))
      (for [m (, "settings" "subcommand" "args" "kwargs")]
           (assoc (getattr self (mangle (+ "m/" m))) "current" (D {})))
      (setv self.m/args.called [])
            self.m/kwargs.called (D {})
      (if world
          (for [store (.chain- self)]
               (if args (setv store.m/args.world []))
               (if kwargs (setv store.m/kwargs.world (D {})))))
      (if instantiated
          (do (if args (setv self.m/args.instantiated []))
              (if kwargs (setv self.m/args.instantiated (D {})))))
      (if baked
          (do (if args
                  (if all-subs
                      (do (setv self.m/args.baked (D {}))
                          (assoc self.m/args.baked self.m/subcommand.default []))
                          (assoc self.m/args.baked subcommand [])))
              (if kwargs
                  (if all-subs
                      (do (setv self.m/kwargs.baked (D {}))
                          (assoc self.m/kwargs.baked self.m/subcommand.default (D {})))
                          (assoc self.m/kwargs.baked subcommand (D {}))))))
      (if set-defaults (.var/set-defaults self)))

(defn var/process-all [self #* args #** kwargs]
      (.var/process-args self #* self.m/args.world)
      (.var/process-args self #* self.m/args.instantiated)
      (.var/process-args self #* (. self m/args baked [self.m/subcommand.current.unprocessed]))
      (.var/process-args self #* args)

      (.var/process-kwargs self #** self.m/kwargs.world)
      (.var/process-kwargs self #** self.m/kwargs.instantiated)
      (.var/process-kwargs self #** (. self m/kwargs baked [self.m/subcommand.current.unprocessed]))
      (.var/process-kwargs self #** kwargs))

(defn var/process-args [self #* args [starter False]]
      (for [arg args]
           (if (isinstance arg (tuple self.m/type-groups.acceptable-args))
               (if (isinstance (. self m/args current unprocessed [(if starter "starter" "regular")]) list)
                   (.append (. self m/args current unprocessed [(if starter "starter" "regular")]) arg)
                   (assoc self.m/args.current.unprocessed (if starter "starter" "regular") [arg]))
               (setv self.m/settings.current.m/frozen True))))

(defn var/process-kwargs [self #** kwargs]
      (defn inner [itr [starter False]]
            (for [[key value] (.items itr)]
                 (if (setx var/process/key-prefix (.cls/is-attr self.__class__ key))
                     (let [var/process/key (.cls/process-attr self.__class__ key var/process/key-prefix)]
                          (cond [(= var/process/key "m/starter-args")
                                 (.var/process-args self #* (if (isinstance value str) (, value) value) :starter True)]
                                [(= var/process/key "m/starter-kwargs") (inner value :starter True)]

[(= var/process/key "m/regular-args") (.var/process-args self #* value)]

[(= var/process/key "m/regular-kwargs") (inner value)]

[(let [trimmed-attr (-> self.__class__ (.cls/trim-attr-prefix var/process/key) (get 1))]
      (and (not (in trimmed-attr self.m/type-groups.excluded-classes))
           (class? (setx literal-attr (.get (globals) trimmed-attr (getattr builtins trimmed-attr None))))
           value))
 (setv self.m/settings.current.m/type literal-attr)]

[True (if (not (in var/process/key (, "m/subcommand")))
                                    (assoc self.m/settings.current key value))]))
               (assoc (. self m/kwargs current unprocessed [(if starter "starter" "regular")]) key value))))
(inner kwargs))

(defn var/apply [self]
    (for [[key value] (.items self.m/settings.current)]
         (setattr self key value)))

(defn command/reset [self]
      (if (not self.m/frozen)
          (setv self.m/command (tea))))

(defn command/process-all [self]
      (for [i (range 2)]
           (.command/process-args self :starter i)
           (.command/process-kwargs self :starter i)))

(defn command/process-args [self [starter False]]
      (for [arg (. self m/args current unprocessed [(if starter "starter" "regular")])]
           (setv command/process-args/arg (cond [(isinstance arg self.m/type-groups.genstrings) (arg)]
                                                [(isinstance arg int) (str arg)]
                                                [(isinstance arg self.__class__) (arg :m/type str)]
                                                [True arg]))
           (if (isinstance (. self m/args current processed [(if starter "starter" "regular")]) list)
               (.append (. self m/args current processed [(if starter "starter" "regular")]) command/process-args/arg)
               (assoc self.m/args.current.processed (if starter "starter" "regular") [command/process-args/arg]))))

(defn command/process-kwargs [self [starter False]]
      (defn inner [value]
            (setv new-value (cond [(isinstance value self.m/type-groups.genstrings) (value)]

[(isinstance value bool) None]
[(isinstance value int) (str value)]

[(isinstance value self.__class__) (value :m/type str)]
                            [True value]))
      (return new-value))
(for [[key value] (.items (. self m/kwargs current unprocessed [(if starter "starter" "regular")]))]
     (if value
         (let [aa (tuple (+ self.m/type-groups.acceptable-args [dict bool]))]
              (if (isinstance value aa)
                  (if (isinstance value dict)
                      (let [no-value-options ["repeat" "repeat-with-values" "rwv"]
                            options (+ no-value-options ["fixed" "dos" "one-dash" "value"])
                            dct-value (.get value "value" None)]
                           (cond [dct-value (setv command/process-kwargs/value (inner dct-value))]
                                 [(any (gfor o (.keys value) (in o no-value-options))) (setv command/process-kwargs/value None)]
                                 [True (raise (AttributeError #[f[Sorry! You must use the "value" keyword if you do not use any of the following: {(.join ", " no-value-options)}]f]))])
                           (for [[k v] (.items value)]
                                 (if (in k options)
                                     (if v
                                         (setv command/process-kwargs/key (if (or (= k "fixed")
                                                                                  self.m/fixed)
                                                                              key
                                                                              (.replace (unmangle key) "_" "-"))
                                               command/process-kwargs/key (cond [(or (= k "dos")
                                                                                     self.m/dos)
                                                                                 (+ "/" command/process-kwargs/key)]
                                                                                [(or (= k "one-dash")
                                                                                     self.m/one-dash
                                                                                     (= (len command/process-kwargs/key) 1))
                                                                                 (+ "-" command/process-kwargs/key)]
                                                                                [True (+ "--" command/process-kwargs/key)])
                                               command/process-kwargs/key-values (cond [(= k "repeat") (lfor i (range v) command/process-kwargs/key)]
                                                                                       [(in k (, "repeat-with-values" "rwv"))
                                                                                        (do (setv key-values [])
                                                                                            (for [j v]
                                                                                                 (.append key-values command/process-kwargs/key)
                                                                                                 (if (setx l (inner j))
                                                                                                     (do (if (isinstance (. self
                                                                                                                            m/kwargs
                                                                                                                            current
                                                                                                                            processed
                                                                                                                            [(if starter
                                                                                                                                 "starter-values"
                                                                                                                                 "regular-values")]) list)
                                                                                                             (.append (. self
                                                                                                                         m/kwargs
                                                                                                                         current
                                                                                                                         processed
                                                                                                                         [(if starter
                                                                                                                              "starter-values"
                                                                                                                              "regular-values")]) l)
                                                                                                             (assoc self.m/kwargs.current.processed
                                                                                                                    (if starter
                                                                                                                        "starter-values"
                                                                                                                        "regular-values") [l]))
                                                                                                         (.append key-values l))))
                                                                                            key-values)]
                                                                                       [True None]))
                                         (setv command/process-kwargs/key None
                                               command/process-kwargs/value None
                                               command/process-kwargs/key-values None))
                                     (raise (AttributeError #[f[Sorry! A keyword argument value of type dict can only have the following keys: {(.join ", " options)}]f])))))
                        [True (setv command/process-kwargs/value (inner value)
                                    command/process-kwargs/key (if self.m/fixed key (.replace (unmangle key) "_" "-"))
                                    command/process-kwargs/key (cond [self.m/dos (+ "/" command/process-kwargs/key)]
                                                                     [(or self.m/one-dash
                                                                          (= (len command/process-kwargs/key) 1))
                                                                      (+ "-" command/process-kwargs/key)]
                                                                     [True (+ "--" command/process-kwargs/key)])
                                    command/process-kwargs/key-values None)])
                  (raise (TypeError #[f[Sorry! Keyword argument value "{value}" of type "{(type value)}" must be one of the following types: {(.join ", " (gfor arg aa arg.__name__))}]f])))
     (if (or command/process-kwargs/key-values
             command/process-kwargs/key)
         (do (if (isinstance (. self m/kwargs current processed [(if starter "starter" "regular")]) list)
                 (if command/process-kwargs/key-values
                     (.extend (. self m/kwargs current processed [(if starter "starter" "regular")]) command/process-kwargs/key-values)
                     (.append (. self m/kwargs current processed [(if starter "starter" "regular")]) command/process-kwargs/key))
                 (if command/process-kwargs/key-values
                     (assoc self.m/kwargs.current.processed (if starter "starter" "regular") command/process-kwargs/key-values)
                     (assoc self.m/kwargs.current.processed (if starter "starter" "regular") [command/process-kwargs/key])))))
     (if (and command/process-kwargs/value
              (not command/process-kwargs/key-values))
         (do (if (isinstance (. self
                                m/kwargs
                                current
                                processed
                                [(if starter
                                     "starter-values"
                                     "regular-values")]) list)
                 (.append (. self
                             m/kwargs
                             current
                             processed
                             [(if starter
                                  "starter-values"
                                  "regular-values")]) command/process-kwargs/value)
                 (assoc self.m/kwargs.current.processed
                       (if starter
                           "starter-values"
                           "regular-values") [command/process-kwargs/value]))
             (if (isinstance (. self
                                m/kwargs
                                current
                                processed
                                [(if starter
                                     "starter"
                                     "regular")]) list)
                 (.append (. self
                             m/kwargs
                             current
                             processed
                             [(if starter
                                  "starter"
                                  "regular")]) command/process-kwargs/value)
                 (assoc self.m/kwargs.current.processed
                       (if starter
                           "starter"
                           "regular") [command/process-kwargs/value]))))))))

(defn command/create [self]
      (if self.m/sudo
          (if (isinstance self.m/sudo bool)
              (.append self.m/command "sudo")
              (.append self.m/command f"sudo -{(-> self.m/sudo (.keys) (iter) (next))} -u {(-> self.m/sudo (.values) (iter) (next))}")))

      (if self.m/shell
          (do (.extend self.m/command self.m/shell "-c" "'")
              (if self.m/run-as
                  (do (.glue self.m/command self.m/run-as)
                      (if self.m/freezer
                          (.extend self.m/command #* self.m/freezer)
                          (.append self.m/command self.m/program)))
                  (if self.m/freezer
                      (do (.glue self.m/command (first self.m/freezer))
                          (.extend self.m/command (cut self.m/freezer 1 -1)))
                      (.glue self.m/command self.m/program))))
          (if self.m/freezer
              (.extend self.m/command self.m/run-as #* self.m/freezer)
              (.extend self.m/command self.m/run-as self.m/program)))

      (.extend self.m/command #* self.m/kwargs.current.processed.starter)
      (if (!= self.m/subcommand.default self.m/subcommand.current.unprocessed)
          (.append self.m/command self.m/subcommand.current.processed))
      (.extend self.m/command
               #* self.m/args.current.processed.starter
               #* self.m/kwargs.current.processed.regular
               #* self.m/args.current.processed.regular)
      (if self.m/shell (.glue self.m/command "'"))
      (if self.m/tiered
          (let [tier "{{ b.t }}"
                replacements (+ self.m/kwargs.current.processed.starter-values
                                self.m/args.current.processed.starter
                                self.m/kwargs.current.processed.regular-values
                                self.m/args.current.processed.regular)
                to-be-replaced (.count (.values self.m/command) tier)]
               (if (= to-be-replaced (len replacements))
                   (for [[index kv] (.items self.m/command :indexed True)]
                        (if (= kv.value tier)
                            (assoc self.m/command kv.key (get replacements index)))))
                   (raise (ValueError "Sorry! The number of tiered replacements must be equal to the number of arguments provided!")))))

(defn return/output [self]
      (cond [self.m/frozen (return (deepcopy self))]
            [self.m/return-command (return (.m/command self))]
            [True (let [output (.return/process self)]
                       (if (isinstance output dict)
                           (do (setv output.stderr (peekable output.stderr)
                                     stds (, "out" "err"))
                               (try (setv peek-value (.peek output.stderr))
                                    (except [StopIteration]
                                            (setv peek-value None)))
                               (if (and peek-value
                                        (not self.m/ignore-stderr)
                                        (not self.m/stdout-stderr))
                                   (raise (SystemError (+ f"In trying to run `{(.m/command self)}':\n\n" (.join "\n" output.stderr)))))
                               (for [[std opp] (zip stds (py "stds[::-1]"))]
                                    (setv stdstd (+ "std" std)
                                          stdopp (+ "std" opp))
                                    (if (< self.m/verbosity 1)
                                        (if (= self.m/capture stdstd)
                                            (del (get output stdopp)))))))
                       (return output))]))

(defn return/process [self]
    (if (.m/command self)
        (do (setv process (.m/popen-partial self))
            (cond [(is self.m/wait None) (with [p (process :pp-stdout DEVNULL :pp-stderr DEVNULL)] (return None))]
                  [self.m/wait (with [p (process)]
                                     (setv return/process/return (D {}))
                                     (for [std (, "out" "err")]
                                          (setv chained []
                                                stdstd (+ "std" std))
                                          (if (setx output (getattr p stdstd))
                                              (for [line output] (setv chained (chain
                                                   chained
                                                   [(if (isinstance line (, bytes bytearray)) (.strip (.decode line "utf-8")) (.strip line))]))))
                                              (assoc return/process/return stdstd (iter chained)))
                                     (.wait p)
                                     (if (> self.m/verbosity 0)
                                         (setv return/process/return.returns.code p.returncode
                                               ;; return/process/return.returns.codes p.returncodes
                                               return/process/return.command.bakery (.m/command self)
                                               return/process/return.command.subprocess p.args
                                               return/process/return.pid p.pid))
                                     (if (> self.m/verbosity 1)
                                         (setv return/process/return.tea self.m/command
                                               return/process/return.subcommand self.m/subcommand))
                                     (let [trim-part (partial trim :last self.m/trim.last
                                                                   :number self.m/trim.number)]
                                          (if (in self.m/trim.std (, "stdout" "both"))
                                              (setv return/process/return.stdout (trim-part :iterable return/process/return.stdout)))
                                          (if (in self.m/trim.std (, "stderr" "both"))
                                              (setv return/process/return.stderr (trim-part :iterable return/process/return.stderr))))
                                     (return return/process/return))]
                  [True (return (process))]))
        (return None)))

(defn return/frosting [self]
      (if (setx output (.return/output self))
          (do (if self.m/frozen (return output))
              (setv frosted-output (if (and (isinstance output dict)
                                            (= (len output) 1))
                                       (-> output (.values) (iter) (next))
                                       output)
                    dict-like-frosted-output (isinstance frosted-output dict)
                    frosted-output (if self.m/dazzle
                                       (cond [dict-like-frosted-output frosted-output]
                                             [(coll? frosted-output) (tuple frosted-output)]
                                             [True [frosted-output]])
                                       frosted-output))
              (if self.m/print-command-and-run (print (.m/command self)))
              (cond [self.m/print-command (print frosted-output)]
                    [self.m/dazzle (if dict-like-frosted-output
                                       (for [cat frosted-output]
                                            (setv outcat (get output cat))
                                            (if (or (isinstance outcat int)
                                                    (isinstance outcat str))
                                                (print f"{cat}: {outcat}")
                                                (do (if (not (in cat self.m/captures))
                                                        (print (+ cat ": ")))
                                                    (if (= cat "return-codes")
                                                        (print outcat)
                                                        (for [line outcat]
                                                             (print line))))))
                                       (for [line frosted-output]
                                            (print line)))])
              (cond [dict-like-frosted-output
                     (for [std (, "out" "err")]
                          (setv stdstd (+ "std" std))
                          (if (hasattr frosted-output stdstd)
                              (do (setv new-frosted-output (get frosted-output stdstd))
                                  (if self.m/split
                                      (setv new-frosted-output (split-and-flatten new-frosted-output)))
                                  (assoc frosted-output stdstd (.m/convert-type self new-frosted-output))))
                          (else (return new-frosted-output)))]
                    [True (let [new-frosted-output (frosting frosted-output self.m/capture)]
                               (if self.m/split
                                   (setv new-frosted-output (split-and-flatten new-frosted-output)))
                               (return (.m/convert-type self new-frosted-output)))]))
          (return None)))

(defn m/popen-partial [self [stdout None] [stderr None]]
      (setv pp-stdout (cond [stdout]
                            [(= self.m/capture "stderr") (.get self.m/popen "stdout" DEVNULL)]
                            [(= self.m/capture "run") (.get self.m/popen "stdout" None)]
                            [True (if self.m/ignore-stdout
                                      (.get self.m/popen "stdout" DEVNULL)
                                      (.get self.m/popen "stdout" PIPE))])
            pp-stderr (or stderr (if (= self.m/capture "run")
                                     (.get self.m/popen "stderr" None)
                                     (cond [self.m/stdout-stderr (.get self.m/popen "stderr" STDOUT)]
                                           [self.m/ignore-stderr (.get self.m/popen "stderr" DEVNULL)]
                                           [True (.get self.m/popen "stderr" PIPE)])))
            bufsize (.get self.m/popen "bufsize" -1)
            universal-newlines (.get self.m/popen "universal-newlines" None)
            universal-text (if (= bufsize 1)
                               True
                               universal-newlines)
            shell (.get self.m/popen "shell" self.m/intact-command)
            command (.m/command self)

env (or (dict self.m/new-exports) (.copy environ))

executable (.get self.m/popen "executable" None)
      kwargs { "bufsize" bufsize
               "stdin" (.get self.m/popen "stdin" self.m/input)
               "stdout" pp-stdout
               "stderr" pp-stderr
               "executable" executable
               "universal_newlines" universal-text
               "text" universal-text
               "shell" shell })
(.update env self.m/exports)
(assoc kwargs "env" env)
(.update kwargs self.m/popen)
(return (partial Popen
                 (if self.m/intact-command
                     command
                     (if shell
                         (join (split command))
                         (split command)))
                 #** kwargs)))

(defn m/spin [self #* args [subcommand- "supercalifragilisticexpialidocious"] #** kwargs]
      (defn inner [title]
            (setv opts (or self.m/debug (.cls/get-attr self.__class__ kwargs "m/debug" :default self.m/debug))
                  bool-opts {})
            (if (isinstance opts dict)
                (do (.update opts { "title" title })
                    (.inspect- self #** opts))
                (if opts
                    (do (.update bool-opts self.m/default-inspect-kwargs)
                        (.update bool-opts { "title" title })
                        (.inspect- self #** bool-opts)))))
      (try (inner "Setup")
           (.var/setup self #* args :subcommand- subcommand- #** kwargs)

           (inner "Process")
           (.command/process-all self)

           (inner "Create")
           (.command/create self)

           (inner "Return")
           (return (.return/frosting self))

           (finally (inner "Reset")
                    (.m/reset-all self))))

(defn m/apply-pipe-redirect [self pr value]
    (setv is-milcery (isinstance value self.__class__))
    (defn inner [v]
          (let [type-string (.join ", " (gfor t (+ (list self.m/type-groups.genstrings)
                                                   self.m/type-groups.this-class-subclass
                                                   [str]) t.__name__))]
               (return (cond [(isinstance v self.m/type-groups.genstrings) [(v)]]
                             [is-milcery (or v.m/freezer (.values v.m/command) [v.m/base-program])]
                             [(isinstance v str) [v]]
                             [True (raise (NotImplemented f"Sorry! Value '{v}' can only be of the following types: {type-string}"))]))))

(if (isinstance value tuple)
    (if (= (len value) 2)
        (setv processed-value (inner (first value))
              processed-pr (get value 1))
        (raise (NotImplemented "Sorry! A tuple value may only contain 2 items: (value, pr)")))
    (setv processed-value (inner value)
          processed-pr pr))

(setv kwargs {}

freezer- (+ (or self.m/freezer (list (.values self.m/command)) [self.m/base-program]) [processed-pr processed-value]))

(.update kwargs (.cls/remove-if-not-attr self.__class__ self.m/kwargs.world))
(if is-milcery (.update kwargs (.cls/remove-if-not-attr value.__class__ value.m/kwargs.world)))

(.update kwargs (.cls/remove-if-not-attr self.__class__ self.m/kwargs.instantiated))
(if is-milcery (.update kwargs (.cls/remove-if-not-attr value.__class__ value.m/kwargs.instantiated)))

(.update kwargs
         (.cls/remove-if-not-attr self.__class__ (. self m/kwargs baked [(or self.m/subcommand.current.unprocessed self.m/subcommand.default)])))
(if is-milcery
    (.update kwargs (.cls/remove-if-not-attr value.__class__ (. value
                                                                m/kwargs
                                                                baked
                                                                [(or value.m/subcommand.current.unprocessed value.m/subcommand.default)]))))

(.update kwargs (.cls/remove-if-not-attr self.__class__ self.m/kwargs.called))
(if is-milcery (.update kwargs (.cls/remove-if-not-attr value.__class__ value.m/kwargs.called)))

(return (.__class__ self :freezer- freezer-
                         :base-program- self.m/base-program
                         #** kwargs)))

(defn deepcopy- [self #* args [subcommand- "supercalifragilisticexpialidocious"] #** kwargs]
      (setv cls (deepcopy self))
      (.bake- cls #* args :instantiated- True :m/subcommand subcommand- #** kwargs)
      (return cls))

(defn check- [self] (return (check self self.m/program)))

(defn freeze- [self] (setv self.m/frozen True))

(defn defrost- [self] (setv self.m/frozen self.m/settings.m/frozen))

(defn bake- [self #* args [subcommand- "supercalifragilisticexpialidocious"] [instantiated- False] #** kwargs ]
      (.extend (if instantiated-
                   self.m/args.instantiated
                   (. self m/args baked [subcommand-])) args)
      (.update (if instantiated-
                   self.m/kwargs.instantiated
                   (. self m/kwargs baked [subcommand-])) kwargs))

(defn bake-all- [self #* args #** kwargs ]
      (for [store (.chain- self)]
           (.extend store.m/args.world args)
           (.update store.m/kwargs.world kwargs)))

(defn splat- [self [set-defaults False] #** kwargs] (.reset- self :baked True :set-defaults set-defaults))

(defn splat-all- [self [set-defaults False] #** kwargs]
      (for [store (.chain- self)]
           (.reset- self :set-defaults set-defaults #** kwargs)))

(defn current-values- [self]
      (setv sd (D { "__slots__" (recursive-unmangle (dfor var
                                                         self.__slots__
                                                         :if (!= var "__dict__")
                                                         [var (getattr self var)])) }))
      (if (hasattr self "__dict__")
          (setv sd.__dict__ self.__dict__))
      (return sd))

(defn inspect- [self #** kwargs] 
      (if (not kwargs)
          (setv kwargs self.m/default-inspect-kwargs))
      (inspect self #** kwargs))

(defn origin- [self] (return (. (first self.__class__.m/stores) __callback__)))

(defn chain- [self] (return (lfor store self.__class__.m/stores store.__callback__)))

(defn __call__ [
        self
        #* args
        [args-before-func (,)]
        #** kwargs ]
    (if (and (not self.m/gitea.off)
             (or self.m/gitea.bool
                 (in self.m/base-program self.m/gitea.list)))
        (return (.deepcopy- self :m/starter-args args :m/starter-kwargs kwargs))
        (cond [(or (.cls/get-attr self.__class__ kwargs "m/context" False)
                   (.cls/get-attr self.__class__ kwargs "m/c" False))
               (return (.deepcopy- self #* args  #** kwargs))]
              [True (return (.m/spin self #* args  #** kwargs))])))

(defn __setattr__ [self attr value] (.__setattr__ (super) (.cls/process-if-attr self.__class__ attr) value))

(defn __getattr__ [self subcommand]
    (if (setx attr (.cls/process-if-attr self.__class__ subcommand :return-bool True))
        (getattr self __getattr__/attr (raise (AttributeError f"Sorry! `{(unmangle subcommand)}' doesn't exist as an attribute!")))
        (do (defn inner [
                    #* args
                    [args-before-func (,)]
                    #** kwargs ]
                  (cond [(or (.cls/get-attr self.__class__ kwargs "m/context" False)
                             (.cls/get-attr self.__class__ kwargs "m/c" False))
                         (return (.deepcopy- self #* args :subcommand- subcommand #** kwargs))]
                        [True (return (.m/spin self #* args :subcommand- subcommand #** kwargs))]))
            (return inner))))

(defn __copy__ [self]

(setv cls self.__class__
      result (.__new__ cls cls)

slots (.from-iterable chain (lfor s self.__class__.__mro__ (getattr s "__slots__" []))))

(for [var slots] (if (not (in var (, "__weakref__"))) (setattr result var (copy (getattr self var)))))
(if (hasattr self "__dict__")
    (.update result.__dict__ self.__dict__))

(setv result.m/frozen result.m/settings.defaults.m/frozen)

(return result))

(defn __deepcopy__ [self memo]

(setv cls self.__class__
      result (.__new__ cls cls))

(assoc memo (id self) result)

(if (and (hasattr self "m/cache") self.m/cache) (assoc memo (id self.m/cache) (.__new__ self.m/cache dict)))

(setv slots (.from-iterable chain (lfor s self.__class__.__mro__ (getattr s "__slots__" []))))

(for [var slots]
     (if (not (in var (, "__weakref__")))
         (setattr result var (deepcopy (getattr self var) memo))))
(if (hasattr self "__dict__")
    (for [[k v] (.items self.__dict__)] (setattr result k (deepcopy v memo))))

(setv result.m/frozen result.m/settings.defaults.m/frozen)

(return result))

(defn __iter__ [self] (yield-from (.m/spin self)))

(defn __or__ [self value] (return (.m/apply-pipe-redirect self "|" value)))

(defn __and__ [self value] (return (.m/apply-pipe-redirect self "| tee" value)))

(defn __add__ [self value] (return (.m/apply-pipe-redirect self "| tee -a" value)))

(defn __lt__ [self value] (return (.m/apply-pipe-redirect self "<" value)))

(defn __lshift__ [self value] (return (.m/apply-pipe-redirect self "<<" value)))

(defn __gt__ [self value] (return (.m/apply-pipe-redirect self ">" value)))

(defn __rshift__ [self value] (return (.m/apply-pipe-redirect self ">>" value)))

(defn __or__ [self value] (return (.m/apply-pipe-redirect self "|" value)))

(defn __and__ [self value] (return (.m/apply-pipe-redirect self "| tee" value)))

(defn __add__ [self value] (return (.m/apply-pipe-redirect self "| tee -a" value)))

(defn __lt__ [self value] (return (.m/apply-pipe-redirect self "<" value)))

(defn __lshift__ [self value] (return (.m/apply-pipe-redirect self "<<" value)))

(defn __gt__ [self value] (return (.m/apply-pipe-redirect self ">" value)))

(defn __rshift__ [self value] (return (.m/apply-pipe-redirect self ">>" value)))

(defn __enter__ [self] (return (deepcopy self)))

(defn __exit__ [self exception-type exception-val exception-traceback] False)

)
