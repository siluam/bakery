(import rich.traceback)
(.install rich.traceback :show-locals True)

(import builtins)
(import hy)
(import py)
(import sys)
(import weakref)

(import addict [Dict :as D])
(import ast [literal-eval])
(import autoslot [Slots SlotsMeta])
(import collections [OrderedDict])
(import copy [copy deepcopy])
(import functools [partial wraps])
(import hy [mangle unmangle])
(import inspect [isclass :as class?])
(import itertools [chain filterfalse tee])
(import more-itertools [peekable])
(import oreo [coll? eclair either? flatten get-un-mangled int? recursive-unmangle tea first-last-n])
(import os [environ path :as osPath getcwd])
(import pathlib [Path])
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

(require hyrule [-> assoc unless])

(defn split-and-flatten [iterable delim]
      (flatten (gfor j (flatten iterable)
               (if (isinstance delim bool)
                   (.split j)
                   (.split j (str delim))))))

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

(cond self.dict-like (.__init__ (super) #** self.output)
      self.iterable (.__init__ (super) #* self.output)
      True (.__init__ (super) self.output))

)

(defn __iter__ [self]
      (yield-from (if self.dict-like
                      (get self self.capture)
                      (.values self))))

(defn __call__ [self]
      (return (cond (not self.iterable) self.output
                    self.dict-like (D (.items self))
                    True (.values self))))

)

(defclass melcery [SlotsMeta]

(defn __init__ [cls #* args #** kwargs] (setv cls.m/stores [])))

(defclass milcery [:metaclass melcery]

(setv __slots__ [ "__weakref__" ])

(defn [classmethod] cls/freezer [cls value freezer]
      (cond (not value) (setv freezer [])
            (coll? value)
            (do (unless (isinstance freezer list) (setv freezer []))
                (.extend freezer value)
                (setv freezer (flatten (gfor i freezer :if i i))))
            True (raise (TypeError f"Sorry! The 'm/freezer' can only accept non-string iterables or non-truthy values!")))
      (return freezer))

(defn [classmethod] cls/string-prefix [cls b a] (+ a b))

(defn [classmethod] cls/process-attr [cls attr prefix]
      (setv attr (unmangle attr))
      (if (.startswith attr prefix)
          (.replace attr "_" "-")
          (mangle (.replace (.cls/string-prefix cls (.lstrip attr "_") prefix) "_" "-"))))

(defn [classmethod] cls/is-attr [cls attr]
      (setv attr (unmangle attr))
      (cond (.endswith attr "__") (return "__")
            (.startswith attr "__") (return "internal/")
            (.startswith attr "_") (return "m/")
            (.startswith attr "internal/") (return "internal/")
            (.startswith attr "m/") (return "m/")
            True (return False)))

(defn [classmethod] cls/process-if-attr [cls attr [return-bool False]]
      (setv attr (unmangle attr))
      (return (if (setx prefix (.cls/is-attr cls attr))
                  (mangle (.cls/process-attr cls attr prefix))
                  (if return-bool False (mangle attr)))))

(defn [classmethod] cls/remove-if-not-attr [cls dct] (return (dfor [key value] (.items dct) :if (.cls/is-attr cls key) [ key value ])))

(defn [classmethod] cls/trim-attr-prefix [cls attr]
      (setv attr (unmangle attr))
      (let [prefix (.cls/is-attr cls attr)]
           (return #(prefix (if prefix (mangle (.removeprefix attr prefix)) (mangle attr))))))

(defn [classmethod] cls/get-attr [cls dct attr [default False]]
      (setv attr (unmangle attr))
      (setv [prefix cls/get-attr/attr] (.cls/trim-attr-prefix cls attr))
      (return (or (.get dct (mangle (+ "__" cls/get-attr/attr)) False)
                  (.get dct (mangle (+ "_" cls/get-attr/attr)) False)
                  (.get dct (mangle (+ "internal/" cls/get-attr/attr)) False)
                  (.get dct (mangle (+ "m/" cls/get-attr/attr)) default))))

(defn [property] m/freezer [self] (return self.internal/freezer))
(defn [m/freezer.setter] m/freezer [self value] (setv self.internal/freezer (.cls/freezer self.__class__ value self.internal/freezer)))

(defn [property] m/frozen [self] (return self.internal/frozen))
(defn [m/frozen.setter] m/frozen [self value] (setv self.internal/frozen (bool value)) (when value (setv self.m/return-output True)))

(defn [property] m/model [self] (return self.internal/model))
(defn [m/model.setter] m/model [self value] (setv self.internal/model (bool value)) (when value (setv self.m/return-output True)))

(defn [property] m/call [self] (return self.internal/call))
(defn [m/call.setter] m/call [self value] (setv self.internal/call (bool value)) (when value (setv self.m/return-output True)))

(defn [property] m/return-command [self] (return self.internal/return-command))
(defn [m/return-command.setter] m/return-command [self value] (setv self.internal/return-command (bool value)) (when value (setv self.m/type str)))

(defn [property] m/print-command [self] (return self.internal/print-command))
(defn [m/print-command.setter] m/print-command [self value] (setv self.internal/print-command (bool value)) (when value (setv self.m/return-command True)))

(defn [property] m/run [self] (return (= self.m/capture "run")))
(defn [m/run.setter] m/run [self value] (when value (setv self.m/capture "run")))

(defn [property] m/sort [self] (return self.internal/sort))
(defn [m/sort.setter] m/sort [self value]
      (when (or (is value None) value)
            (setv dict-like (isinstance value dict)
                  iterable (coll? value)
                  reverse-default False
                  key-default None
                  self.internal/sort (D { "reverse" (cond dict-like (.get value "reverse" reverse-default)
                                                          iterable (get (or (lfor item value :if (isinstance item bool) item) #(reverse-default)) 0)
                                                          (isinstance value bool) value
                                                          True reverse-default)
                                          "key" (cond dict-like (.get value "key" key-default)
                                                      iterable (get (or (lfor item value :if (callable item) item) #(key-default)) 0)
                                                      (callable value) value
                                                      True key-default) }))))

(defn [property] m/filter [self] (return self.internal/filter))
(defn [m/filter.setter] m/filter [self value]
      (when (or (is value None) value)
            (setv dict-like (isinstance value dict)
                  iterable (coll? value)
                  reverse-default False
                  key-default None
                  self.internal/filter (D { "reverse" (cond dict-like (.get value "reverse" reverse-default)
                                                            iterable (get (or (lfor item value :if (isinstance item bool) item) #(reverse-default)) 0)
                                                            (isinstance value bool) value
                                                            True reverse-default)
                                            "key" (cond dict-like (.get value "key" key-default)
                                                        iterable (get (or (lfor item value :if (callable item) item) #(key-default)) 0)
                                                        (callable value) value
                                                        True key-default) }))))

(defn [property] m/n-lines [self] (return self.internal/n-lines))
(defn [m/n-lines.setter] m/n-lines [self value]
      (setv dict-like (isinstance value dict)
            iterable (coll? value)
            last-default False
            number-default 0
            std-default "stdout"
            std (cond dict-like (.get value "std" std-default)
                      iterable (get (or (lfor item value :if (isinstance item str) item) #(std-default)) 0)
                      (isinstance value str) value
                      True std-default)
            self.internal/n-lines (D {

                                        "last" (cond dict-like (.get value "last" last-default)
                                                     iterable (get (or (lfor item value :if (isinstance item bool) item) #(last-default)) 0)
                                                     (isinstance value bool) value
                                                     True last-default)
                                        "number" (cond dict-like (.get value "number" number-default)
                                                       iterable (get (or (lfor item value :if (int? item) item) #(number-default)) 0)
                                                       (int? value) value
                                                       True number-default)

                                        "std" (when std (if (in std (setx stds #("stdout" "stderr" "both")))
                                                         std
                                                         (raise (TypeError #[f[Sorry! You must choose an `std' value from: {(.join ", " stds)}]f]))))})))

(defn [property] m/c [self] (return self.m/context))
(defn [m/c.setter] m/c [self value] (setv self.m/context (bool value)))

(defn [property] m/capture [self] (return self.internal/capture))
(defn [m/capture.setter] m/capture [self value]
      (if (in value self.m/captures)
          (setv self.internal/capture value)
          (raise (TypeError #[f[Sorry! Capture type "{value}" is not permitted! Choose from one of: {(.join ", " self.m/captures)}]f]))))

(defn [property] m/sudo [self] (return self.internal/sudo))
(defn [m/sudo.setter] m/sudo [self value]
      (setv error-message #[[Sorry! `m/sudo' must be a string of "i" or "s", or a dict-like object of length 1, key "i" or "s", and value `user', or a boolean!]]
            self.internal/sudo (if value
                                   (if (or (isinstance value bool) (= (len value) 1))
                                       (cond (isinstance value str) (if (in value #("i" "s")) { value "root" } (raise (ValueError error-message)))
                                             (isinstance value bool) value
                                             (isinstance value dict) (if (-> value (.keys) (iter) (next) (in #("i" "s"))) value (raise (ValueError error-message))))
                                       (raise (ValueError error-message)))
                                   False)))

(defn [property] m/exports [self] (return self.internal/exports))
(defn [m/exports.setter] m/exports [self value]
      (setv self.internal/exports value)
      (when value (setv self.m/intact-command (bool value))))

(defn [property] m/new-exports [self] (return self.internal/new-exports))
(defn [m/new-exports.setter] m/new-exports [self value]
      (setv self.internal/new-exports value)
      (when value (setv self.m/intact-command (bool value))))

(defn __init__ [
        self
        #* args
        [program- None]
        [base-program- None]
        [freezer- None]
        #** kwargs]

(.append self.__class__.m/stores (.ref weakref self self))

(setv self.m/type-groups (D {}))

(setv self.m/type-groups.acceptable-args [str int Path py._path.local.LocalPath])

(setv self.m/type-groups.reprs #("str" "repr"))

(setv self.m/type-groups.this-class-subclass [self.__class__])
(.extend self.m/type-groups.acceptable-args self.m/type-groups.this-class-subclass)

(setv self.m/type-groups.genstrings [tea])
(.extend self.m/type-groups.acceptable-args self.m/type-groups.genstrings)
(setv self.m/type-groups.genstrings (tuple self.m/type-groups.genstrings))

(setv self.m/type-groups.excluded-classes #("type" "filter"))

(setv self.m/subcommand (D {})
      self.m/subcommand.default "supercalifragilisticexpialidocious"
      self.m/subcommand.current (D {})
      self.m/subcommand.current.unprocessed self.m/subcommand.default
      self.m/subcommand.current.intact False
      self.m/subcommand.current.processed self.m/subcommand.default)

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
        (when (in "--" self.m/program)
              (setv self.m/program (.join osPath (getcwd) (.replace self.m/program "--" "."))))
        (unless (check self self.m/program)
                (raise (ImportError f"cannot import name '{self.m/program}' from '{self.__class__.__module__}'")))
        (setv self.m/base-program (or base-program- self.m/program)))
    (setv self.m/program ""
          self.m/base-program (or base-program- self.m/program)))

(setv self.m/return-categories #(
    "stdout"
    "stderr"
    "return-codes"
    "command"
    "tea"
    "verbosity"
))

(setv self.m/command (tea))

(setv self.m/gitea (D {})
      self.m/gitea.list [ "git" "yadm" "tailapi" ]
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

(setv self.m/return-output False)
(setv self.m/settings.defaults.m/return-output (deepcopy self.m/return-output))

(setv self.internal/frozen False)
(setv self.m/settings.defaults.m/frozen (deepcopy self.internal/frozen))

(setv self.internal/model False)
(setv self.m/settings.defaults.m/model (deepcopy self.internal/model))

(setv self.internal/call False)
(setv self.m/settings.defaults.m/call (deepcopy self.internal/call))

(setv self.m/captures #("stdout" "stderr" "both" "run"))
(setv self.internal/capture "stdout")
(setv self.m/settings.defaults.m/capture (deepcopy self.internal/capture))

(setv self.m/shell None)
(setv self.m/settings.defaults.m/shell (deepcopy self.m/shell))

(setv self.m/dazzle False)
(setv self.m/settings.defaults.m/dazzle (deepcopy self.m/dazzle))

(setv self.m/dazzling None)
(setv self.m/settings.defaults.m/dazzling (deepcopy self.m/dazzling))

(setv self.m/ignore-stdout False)
(setv self.m/settings.defaults.m/ignore-stdout (deepcopy self.m/ignore-stdout))

(setv self.m/ignore-stderr False)
(setv self.m/settings.defaults.m/ignore-stderr (deepcopy self.m/ignore-stderr))

(setv self.m/stdout-stderr False)
(setv self.m/settings.defaults.m/stdout-stderr (deepcopy self.m/stdout-stderr))

(setv self.m/false-error False)
(setv self.m/settings.defaults.m/false-error (deepcopy self.m/false-error))

(setv self.m/replace-error False)
(setv self.m/settings.defaults.m/replace-error (deepcopy self.m/replace-error))

(setv self.m/verbosity 0)
(setv self.m/settings.defaults.m/verbosity (deepcopy self.m/verbosity))

(setv self.m/run-as "")
(setv self.m/settings.defaults.m/run-as (deepcopy self.m/run-as))

(setv self.internal/n-lines (D { "last" "False" "number" 0 "std" "stdout" }))
(setv self.m/settings.defaults.m/n-lines (deepcopy self.internal/n-lines))

(setv self.internal/sort False)
(setv self.m/settings.defaults.m/sort (deepcopy self.internal/sort))

(setv self.internal/filter False)
(setv self.m/settings.defaults.m/filter (deepcopy self.internal/filter))

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

(setv self.m/regular-args #())
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

(setv self.m/split-after False)
(setv self.m/settings.defaults.m/split-after (deepcopy self.m/split-after))

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

(setv self.m/sort-then-filter False)
(setv self.m/settings.defaults.m/sort-then-filter (deepcopy self.m/sort-then-filter))

)

(defn misc/type-name-is-string [self [type/type None]]
      (return (in (. (or type/type self.m/type) __name__) self.m/type-groups.reprs)))

(defn m/reset-all [self]
      (.reset- self)
      (.command/reset self))

(defn ct/filter [self input]
      (when self.m/filter
            (setv string-like (isinstance input str)
                  input (if self.m/filter.reverse
                            (tuple (filterfalse self.m/filter.key input))
                            (tuple (filter self.m/filter.key input))))
            (when string-like (setv input (.join "" input))))
      input)

(defn ct/sort [self input]
      (when self.m/sort
            (setv string-like (isinstance input str)
                  input (sorted input #** self.m/sort))
            (when string-like (setv input (.join "" input))))
      input)

(defn ct/convert [self input [type/type None]]
      (setv type/type/type (or type/type self.m/type))
      (if input
          (do (when (isinstance input self.m/type-groups.genstrings)
                    (let [frosted-input (input)]
                         (cond (isinstance frosted-input str) (setv input [(.fill (TextWrapper :break-long-words False :break-on-hyphens False) frosted-input)])
                               (isinstance frosted-input int) (if (.misc/type-name-is-string self :type/type type/type/type)
                                                                  (return (pretty-repr frosted-input))
                                                                  (return frosted-input)))))
              (setv input (if self.m/sort-then-filter
                              (.ct/filter self (.ct/sort self input))
                              (.ct/sort self (.ct/filter self input))))
              (return (cond (and self.m/progress (coll? input)) (eclair input (.m/command self) self.m/progress)
                            (.misc/type-name-is-string self :type/type type/type/type) (.join "\n" input)
                            True (if (and self.m/sort (either? type/type/type list)) input (type/type/type input)))))
          (return (type/type/type input))))

(defn subcommand/get [self #** kwargs]
      (setv self.m/subcommand.current.intact (.cls/get-attr self.__class__ kwargs "m/intact-subcommand"))
      (setv subcommand (.cls/get-attr self.__class__ kwargs "m/subcommand" :default self.m/subcommand.default))
      (when (!= subcommand self.m/subcommand.default) (setv self.m/subcommand.current.unprocessed subcommand)))

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
      (unless self.m/subcommand.current.unprocessed
              (setv self.m/subcommand.current.unprocessed self.m/subcommand.default))
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
      (for [m #("settings" "subcommand" "args" "kwargs")]
           (assoc (getattr self (mangle (+ "m/" m))) "current" (D {})))
      (setv self.m/args.called [])
            self.m/kwargs.called (D {})
      (when world
            (for [store (.chain- self)]
                 (when args (setv store.m/args.world []))
                 (when kwargs (setv store.m/kwargs.world (D {})))))
      (when instantiated
            (when args (setv self.m/args.instantiated []))
            (when kwargs (setv self.m/args.instantiated (D {}))))
      (when baked
            (when args
                  (if all-subs
                      (do (setv self.m/args.baked (D {})) (assoc self.m/args.baked self.m/subcommand.default []))
                      (assoc self.m/args.baked subcommand [])))
            (when kwargs
                  (if all-subs
                      (do (setv self.m/kwargs.baked (D {})) (assoc self.m/kwargs.baked self.m/subcommand.default (D {})))
                      (assoc self.m/kwargs.baked subcommand (D {})))))
      (when set-defaults (.var/set-defaults self)))

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
      (let [ sr (if starter "starter" "regular") ]
           (for [arg args]
                (if (isinstance arg (tuple self.m/type-groups.acceptable-args))
                    (if (isinstance (. self m/args current unprocessed [sr]) list)
                        (.append (. self m/args current unprocessed [sr]) arg)
                        (assoc self.m/args.current.unprocessed sr [arg]))
                    (setv self.m/settings.current.m/frozen True)))))

(defn var/process-kwargs [self #** kwargs]
      (defn inner [itr [starter False]]
            (for [[key value] (.items itr)]
                 (if (setx var/process/key-prefix (.cls/is-attr self.__class__ key))
                     (let [var/process/key (.cls/process-attr self.__class__ key var/process/key-prefix)]
                          (cond (= var/process/key "m/starter-args") (.var/process-args self #* (if (isinstance value str) #(value) value) :starter True)
                                (= var/process/key "m/starter-kwargs") (inner value :starter True)

                                (= var/process/key "m/regular-args") (.var/process-args self #* value)

                                (= var/process/key "m/regular-kwargs") (inner value)

                                (let [trimmed-attr (-> self.__class__ (.cls/trim-attr-prefix var/process/key) (get 1))]
                                     (and (not (in trimmed-attr self.m/type-groups.excluded-classes))
                                          (class? (setx literal-attr (.get (globals) trimmed-attr (getattr builtins trimmed-attr None))))
                                          value))
                                (setv self.m/settings.current.m/type literal-attr)

                                True (when (not (in var/process/key #("m/subcommand")))
                                           (assoc self.m/settings.current key value))))
                     (assoc (. self m/kwargs current unprocessed [(if starter "starter" "regular")]) key value))))
      (inner kwargs))

(defn var/apply [self]
    (for [[key value] (.items self.m/settings.current)]
         (setattr self key value)))

(defn command/reset [self] (unless self.m/frozen (setv self.m/command (tea))))

(defn command/process-all [self]
      (for [i (range 2)]
           (.command/process-args self :starter i)
           (.command/process-kwargs self :starter i)))

(defn command/process-args [self [starter False]]
      (let [ sr (if starter "starter" "regular") ]
           (for [arg (. self m/args current unprocessed [sr])]
                (setv command/process-args/arg (cond (isinstance arg self.m/type-groups.genstrings) (arg)
                                                     (isinstance arg int) (str arg)
                                                     (isinstance arg self.__class__) (arg :m/type str)
                                                     True arg))
                (if (isinstance (. self m/args current processed [sr]) list)
                    (.append (. self m/args current processed [sr]) command/process-args/arg)
                    (assoc self.m/args.current.processed sr [command/process-args/arg])))))

(defn command/process-kwargs [self [starter False]]
      (defn inner [value]
            (setv new-value (cond (isinstance value self.m/type-groups.genstrings) (value)

                                  (isinstance value bool) None
                                  (isinstance value int) (str value)

                                  (isinstance value self.__class__) (value :m/type str)
                                  True value))
            (return new-value))
      (setv sr (if starter "starter" "regular"))
      (for [[key value] (.items (. self m/kwargs current unprocessed [sr]))]
           (when value
                 (let [aa (tuple (+ self.m/type-groups.acceptable-args [dict bool]))]
                      (if (isinstance value aa)
                          (if (isinstance value dict)
                              (let [no-value-options ["repeat" "repeat-with-values" "rwv"]
                                    options (+ no-value-options ["fixed" "dos" "one-dash" "value"])
                                    dct-value (.get value "value" None)]
                                   (cond dct-value (setv command/process-kwargs/value (inner dct-value))
                                         (any (gfor o (.keys value) (in o no-value-options))) (setv command/process-kwargs/value None)
                                         True (raise (AttributeError #[f[Sorry! You must use the "value" keyword if you do not use any of the following: {(.join ", " no-value-options)}]f])))
                                   (for [[k v] (.items value)]
                                         (if (in k options)
                                             (if v
                                                 (setv command/process-kwargs/key (if (or (= k "fixed")
                                                                                          self.m/fixed)
                                                                                      key
                                                                                      (.replace (unmangle key) "_" "-"))
                                                       command/process-kwargs/key (cond (or (= k "dos")
                                                                                            self.m/dos)
                                                                                        (+ "/" command/process-kwargs/key)
                                                                                        (or (= k "one-dash")
                                                                                            self.m/one-dash
                                                                                            (= (len command/process-kwargs/key) 1))
                                                                                        (+ "-" command/process-kwargs/key)
                                                                                        True (+ "--" command/process-kwargs/key))
                                                       command/process-kwargs/key-values (cond (= k "repeat")
                                                                                               (lfor i (range v) command/process-kwargs/key)
                                                                                               (in k #("repeat-with-values" "rwv"))
                                                                                               (do (setv key-values [])
                                                                                                   (for [j v]
                                                                                                        (.append key-values command/process-kwargs/key)
                                                                                                        (when (setx l (inner j))
                                                                                                            (if (isinstance (. self
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
                                                                                                            (.append key-values l)))
                                                                                                   key-values)))
                                                 (setv command/process-kwargs/key None
                                                       command/process-kwargs/value None
                                                       command/process-kwargs/key-values None))
                                             (raise (AttributeError #[f[Sorry! A keyword argument value of type dict can only have the following keys: {(.join ", " options)}]f])))))
                                (setv command/process-kwargs/value (inner value)
                                      command/process-kwargs/key (if self.m/fixed key (.replace (unmangle key) "_" "-"))
                                      command/process-kwargs/key (cond self.m/dos (+ "/" command/process-kwargs/key)
                                                                       (or self.m/one-dash
                                                                           (= (len command/process-kwargs/key) 1))
                                                                       (+ "-" command/process-kwargs/key)
                                                                       True (+ "--" command/process-kwargs/key))
                                      command/process-kwargs/key-values None))

                          (raise (TypeError #[f[Sorry! Keyword argument value "{value}" of type "{(type value)}" must be one of the following types: {(.join ", " (gfor arg aa arg.__name__))}]f])))))
           (when (or command/process-kwargs/key-values
                     command/process-kwargs/key)
                 (if (isinstance (. self m/kwargs current processed [sr]) list)
                     (if command/process-kwargs/key-values
                         (.extend (. self m/kwargs current processed [sr]) command/process-kwargs/key-values)
                         (.append (. self m/kwargs current processed [sr]) command/process-kwargs/key))
                     (if command/process-kwargs/key-values
                         (assoc self.m/kwargs.current.processed sr command/process-kwargs/key-values)
                         (assoc self.m/kwargs.current.processed sr [command/process-kwargs/key]))))
           (when (and command/process-kwargs/value
                      (not command/process-kwargs/key-values))
                 (if (isinstance (. self
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
                                "regular") [command/process-kwargs/value])))))

(defn command/create [self]
      (when self.m/sudo
            (if (isinstance self.m/sudo bool)
                (.append self.m/command "sudo")
                (.append self.m/command f"sudo -{(-> self.m/sudo (.keys) (iter) (next))} -u {(-> self.m/sudo (.values) (iter) (next))}")))

      (if (and self.m/shell (not self.m/freezer))
          (do (.extend self.m/command self.m/shell "-c" "'")
              (if self.m/run-as
                  (do (.glue self.m/command self.m/run-as)
                      (.append self.m/command self.m/program))
                  (.glue self.m/command self.m/program)))
          (if self.m/run-as
              (.extend self.m/command self.m/run-as self.m/program)
              (.append self.m/command self.m/program)))

      (when self.m/freezer
            (when self.m/shell
                  (for [[index value] (enumerate self.m/freezer)]
                       (when (= (get value -1) "'")
                             (assoc self.m/freezer index (cut value 0 -1)))))
            (.extend self.m/command #* self.m/freezer))

      (.extend self.m/command #* self.m/kwargs.current.processed.starter)
      (when (!= self.m/subcommand.default self.m/subcommand.current.unprocessed) (.append self.m/command self.m/subcommand.current.processed))
      (.extend self.m/command
               #* self.m/args.current.processed.starter
               #* self.m/kwargs.current.processed.regular
               #* self.m/args.current.processed.regular)
      (when self.m/shell (.glue self.m/command "'"))
      (when self.m/tiered
            (let [tier "{{ b.t }}"
                  replacements (+ self.m/kwargs.current.processed.starter-values
                                  self.m/args.current.processed.starter
                                  self.m/kwargs.current.processed.regular-values
                                  self.m/args.current.processed.regular)
                  to-be-replaced (.count (.values self.m/command) tier)]
                 (if (= to-be-replaced (len replacements))
                     (for [[index kv] (.items self.m/command :indexed True)]
                          (when (= kv.value tier)
                                (assoc self.m/command kv.key (get replacements index))))
                     (raise (ValueError "Sorry! The number of tiered replacements must be equal to the number of arguments provided!"))))))

(defn return/output [self]
      (cond self.m/model (return (.return/model self))
            self.m/call (return (.return/call self))
            self.m/frozen (return (deepcopy self))
            self.m/return-command (return (.m/command self))
            True (let [output (.return/process self)]
                      (when (isinstance output dict)
                            (setv output.stderr (peekable output.stderr)
                                  stds #("out" "err"))
                            (try (setv peek-value (.peek output.stderr))
                                 (except [StopIteration]
                                         (setv peek-value None)))
                            (when (and peek-value
                                       (not self.m/ignore-stderr)
                                       (not self.m/stdout-stderr))
                                  (if (or self.m/replace-error self.m/false-error)
                                      (setv (. output ["stdout"]) (or self.m/replace-error False))
                                      (raise (SystemError (+ f"In trying to run `{(.m/command self)}':\n\n" (.join "\n" output.stderr))))))
                            (for [[std opp] (zip stds (py "stds[::-1]"))]
                                 (setv stdstd (+ "std" std)
                                       stdopp (+ "std" opp))
                                 (when (and (< self.m/verbosity 1) (= self.m/capture stdstd)) (del (get output stdopp)))))
                      (return output))))

(defn return/model [self]
      (let [ settings [] ]
           (for [setting self.m/settings.defaults]
                (let [ k (unmangle setting)
                       v (getattr self setting) ]
                     (.append settings (.Keyword hy.models k))
                     (.append settings (cond (= (get (.cls/trim-attr-prefix self.__class__ k) 1) "model") False
                                             (isinstance v D) (._dict_wrapper hy.models v)
                                             (callable v) (.Symbol hy.models v.__name__)
                                             True v))))
           (return (.as-model hy.models `(bakery :program- ~self.m/program
                                                 :base-program- ~self.m/base-program
                                                 :freezer- ~self.m/freezer
                                                 ~@settings)))))

(defn return/call [self]
      (let [ settings "" ]
           (for [setting self.m/settings.defaults]
                (let [ k (unmangle setting)
                       v (getattr self setting) ]
                     (+= settings f" :{k} {(cond (= (get (.cls/trim-attr-prefix self.__class__ k) 1) "call") False
                                                 (and (isinstance v str) (not v)) "''"
                                                 (callable v) v.__name__
                                                 True v)}")))
           (return f"bakery :program- {(or self.m/program "''")} :base-program- {self.m/base-program} :freezer- {self.m/freezer}{settings}")))

(defn return/process [self]
    (if (.m/command self)
        (do (setv process (.m/popen-partial self))
            (cond (is self.m/wait None) (with [p (process :stdout DEVNULL :stderr DEVNULL)] (return None))
                  self.m/wait (with [p (process)]
                                    (setv return/process/return (D {}))
                                    (for [std #("out" "err")]
                                         (setv chained []
                                               stdstd (+ "std" std))
                                         (when (setx output (getattr p stdstd))
                                               (for [line output]
                                                    (setv line (if (isinstance line #(bytes bytearray))
                                                                   (.strip (.decode line "utf-8"))
                                                                   (.strip line))
                                                          chained (chain chained [line]))
                                                    (when (and (= std "out") self.m/dazzling) (print line))))
                                         (assoc return/process/return stdstd (iter chained)))
                                    (.wait p)
                                    (when (> self.m/verbosity 0)
                                          (setv return/process/return.returns.code p.returncode
                                                ;; return/process/return.returns.codes p.returncodes
                                                return/process/return.command.bakery (.m/command self)
                                                return/process/return.command.subprocess p.args
                                                return/process/return.pid p.pid))
                                    (when (> self.m/verbosity 1)
                                          (setv return/process/return.tea self.m/command
                                                return/process/return.subcommand self.m/subcommand))
                                    (let [first-last-n-part (partial first-last-n :last self.m/n-lines.last
                                                                                  :number self.m/n-lines.number)]
                                         (when (in self.m/n-lines.std #("stdout" "both"))
                                               (setv return/process/return.stdout (first-last-n-part :iterable return/process/return.stdout)))
                                         (when (in self.m/n-lines.std #("stderr" "both"))
                                               (setv return/process/return.stderr (first-last-n-part :iterable return/process/return.stderr))))
                                    (return return/process/return))
                  True (return (process))))
        (return None)))

(defn return/frosting [self]
      (if (setx output (.return/output self))
          (do (when self.m/return-output (return output))
              (when (or self.m/replace-error self.m/false-error) (return output.stdout))
              (setv frosted-output (if (and (isinstance output dict)
                                            (= (len output) 1))
                                       (-> output (.values) (iter) (next))
                                       output)
                    dict-like-frosted-output (isinstance frosted-output dict)
                    frosted-output (if self.m/dazzle
                                       (cond dict-like-frosted-output frosted-output
                                             (coll? frosted-output) (tuple frosted-output)
                                             True #(frosted-output))
                                       frosted-output))
              (when self.m/print-command-and-run (print (.m/command self)))
              (cond self.m/print-command (print frosted-output)
                    self.m/dazzle (if dict-like-frosted-output
                                      (for [cat frosted-output]
                                           (setv outcat (get output cat))
                                           (if (or (isinstance outcat int)
                                                   (isinstance outcat str))
                                               (print f"{cat}: {outcat}")
                                               (do (unless (in cat self.m/captures)
                                                           (print (+ cat ": ")))
                                                   (if (= cat "return-codes")
                                                       (print outcat)
                                                       (for [line outcat]
                                                            (print line))))))
                                      (for [line frosted-output]
                                           (print line))))
              (cond dict-like-frosted-output
                    (for [std #("out" "err")]
                         (setv stdstd (+ "std" std))
                         (when (hasattr frosted-output stdstd)
                               (setv processed-output (get frosted-output stdstd))
                               (when self.m/split (setv processed-output (split-and-flatten processed-output self.m/split)))
                               (setv processed-output (.ct/convert self processed-output))
                               (when self.m/split-after (setv processed-output (split-and-flatten processed-output self.m/split-after)))
                               (setv (. frosted-output [stdstd]) processed-output
                                     new-frosted-output frosted-output)))
                    True (do (setv new-frosted-output (frosting frosted-output self.m/capture))
                             (when self.m/split (setv new-frosted-output (split-and-flatten new-frosted-output self.m/split)))
                             (setv new-frosted-output (.ct/convert self new-frosted-output))
                             (when self.m/split-after (setv new-frosted-output (split-and-flatten new-frosted-output self.m/split-after)))))
              (return new-frosted-output))
          (return None)))

(defn m/popen-partial [self [stdout None] [stderr None]]
      (setv pp-stdout (cond stdout stdout
                            (= self.m/capture "stderr") (.get self.m/popen "stdout" DEVNULL)
                            (= self.m/capture "run") (.get self.m/popen "stdout" None)
                            True (if self.m/ignore-stdout
                                     (.get self.m/popen "stdout" DEVNULL)
                                     (.get self.m/popen "stdout" PIPE)))
            pp-stderr (or stderr (if (= self.m/capture "run")
                                     (.get self.m/popen "stderr" None)
                                     (cond self.m/stdout-stderr (.get self.m/popen "stderr" STDOUT)
                                           self.m/ignore-stderr (.get self.m/popen "stderr" DEVNULL)
                                           True (.get self.m/popen "stderr" PIPE))))

            bufsize (.get self.m/popen "bufsize" (when self.m/dazzling 1 -1))
            universal-newlines (.get self.m/popen "universal-newlines" self.m/dazzling)

            universal-text (if (= bufsize 1) True universal-newlines)
            shell (.get self.m/popen "shell" self.m/intact-command)
            command (.m/command self)

            env (or (dict self.m/new-exports) (.copy environ))

            executable (.get self.m/popen "executable" None)
            kwargs { "bufsize" bufsize
                     "stdin" (.get self.m/popen "stdin" self.m/input)
                     "stdout" pp-stdout
                     "stderr" pp-stderr
                     "executable" executable
                     "universal_newlines" universal-newlines
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
                (when opts
                      (.update bool-opts self.m/default-inspect-kwargs)
                      (.update bool-opts { "title" title })
                      (.inspect- self #** bool-opts))))
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
               (return (cond (isinstance v self.m/type-groups.genstrings) [(v)]
                             is-milcery (or v.m/freezer (.values v.m/command) [v.m/base-program])
                             (isinstance v str) [v]
                             True (raise (NotImplemented f"Sorry! Value '{v}' can only be of the following types: {type-string}"))))))

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
    (when is-milcery (.update kwargs (.cls/remove-if-not-attr value.__class__ value.m/kwargs.world)))

    (.update kwargs (.cls/remove-if-not-attr self.__class__ self.m/kwargs.instantiated))
    (when is-milcery (.update kwargs (.cls/remove-if-not-attr value.__class__ value.m/kwargs.instantiated)))

    (.update kwargs
             (.cls/remove-if-not-attr self.__class__ (. self m/kwargs baked [(or self.m/subcommand.current.unprocessed self.m/subcommand.default)])))
    (when is-milcery
          (.update kwargs (.cls/remove-if-not-attr value.__class__ (. value
                                                                      m/kwargs
                                                                      baked
                                                                      [(or value.m/subcommand.current.unprocessed value.m/subcommand.default)]))))

    (.update kwargs (.cls/remove-if-not-attr self.__class__ self.m/kwargs.called))
    (when is-milcery (.update kwargs (.cls/remove-if-not-attr value.__class__ value.m/kwargs.called)))

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
      (when (hasattr self "__dict__") (setv sd.__dict__ (recursive-unmangle self.__dict__)))
      (return sd))

(defn inspect- [self #** kwargs] 
      (unless kwargs
              (setv kwargs self.m/default-inspect-kwargs))
      (inspect self :Hy True #** kwargs))

(defn origin- [self] (return (. (first self.__class__.m/stores) __callback__)))

(defn chain- [self] (return (lfor store self.__class__.m/stores store.__callback__)))

(defn __call__ [
        self
        #* args
        [args-before-func #()]
        #** kwargs ]
    (if (and (not self.m/gitea.off)
             (or self.m/gitea.bool
                 (in self.m/base-program self.m/gitea.list)))
        (return (.deepcopy- self :m/starter-args args :m/starter-kwargs kwargs))
        (cond (or (.cls/get-attr self.__class__ kwargs "m/context" False)
                   (.cls/get-attr self.__class__ kwargs "m/c" False))
               (return (.deepcopy- self #* args  #** kwargs))
              True (return (.m/spin self #* args  #** kwargs)))))

(defn __setattr__ [self attr value] (.__setattr__ (super) (.cls/process-if-attr self.__class__ attr) value))

(defn __getattr__ [self subcommand]
    (if (.cls/process-if-attr self.__class__ subcommand :return-bool True)
        (getattr self __getattr__/attr (raise (AttributeError f"Sorry! `{(unmangle subcommand)}' doesn't exist as an attribute!")))
        (do (defn inner [
                    #* args
                    [args-before-func #()]
                    #** kwargs ]
                  (cond (or (.cls/get-attr self.__class__ kwargs "m/context" False)
                             (.cls/get-attr self.__class__ kwargs "m/c" False))
                         (return (.deepcopy- self #* args :subcommand- subcommand #** kwargs))
                        True (return (.m/spin self #* args :subcommand- subcommand #** kwargs))))
            (return inner))))

(defn __copy__ [self]

    (setv cls self.__class__
          result (.__new__ cls cls)

          slots (.from-iterable chain (lfor s self.__class__.__mro__ (getattr s "__slots__" []))))

    (for [var slots] (unless (in var #("__weakref__")) (setattr result var (copy (getattr self var)))))
    (when (hasattr self "__dict__") (.update result.__dict__ self.__dict__))

    (setv result.m/frozen result.m/settings.defaults.m/frozen)

    (return result))

(defn __deepcopy__ [self memo]

    (setv cls self.__class__
          result (.__new__ cls cls))

    (assoc memo (id self) result)

    (when (and (hasattr self "m/cache") self.m/cache)
          (assoc memo (id self.m/cache) (.__new__ self.m/cache dict)))

    (setv slots (.from-iterable chain (lfor s self.__class__.__mro__ (getattr s "__slots__" []))))

    (for [var slots]
         (when (not (in var #("__weakref__")))
               (setattr result var (deepcopy (getattr self var) memo))))
    (when (hasattr self "__dict__")
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
