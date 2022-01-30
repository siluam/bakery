;; Imports


;; [[file:bakery.org::*Imports][Imports:1]]
(import builtins)
(import pout weakref)
;; Imports:1 ends here

;; For Nuitka


;; [[file:bakery.org::*For Nuitka][For Nuitka:1]]
(import hyrule)
;; For Nuitka:1 ends here

;; From


;; [[file:bakery.org::*From][From:1]]
(import addict [Dict :as D])
(import ast [literal-eval])
(import autoslot [SlotsPlusDictMeta])
(import collections [OrderedDict])
(import copy [copy deepcopy])
(import functools [partial wraps])
(import gensing [frosting tea])
(import hy [mangle unmangle])
(import hyrule [coll?])
(import inspect [isclass :as class?])
(import itertools [chain tee])
(import nanite [fullpath peek trim])
(import os [environ])
(import rich [pretty print inspect])
(import rich.pretty [pretty-repr pprint])
(import shlex [join split])
(import subprocess [DEVNULL PIPE Popen])
(import textwrap [TextWrapper])
(import toml [load])
(import toolz [first])
(import types [MethodType])
(import typing [Any Dict Generator Tuple Union])
;; From:1 ends here

;; Requires


;; [[file:bakery.org::*Requires][Requires:1]]
(require hyrule [-> ->> assoc])
;; Requires:1 ends here

;; The Meta Class

;; Adapted from [[https://stackoverflow.com/a/1800999/10827766][this answer]] by [[https://stackoverflow.com/users/36433/a-coady][A. Coady]], as well as [[https://stackoverflow.com/a/31537249/10827766][this answer]] by [[https://stackoverflow.com/users/302343/timur][Timur]].

;; Remember that ~metaclasses~ use ~cls~ instead of ~self~!


;; [[file:bakery.org::*The Meta Class][The Meta Class:1]]
(defclass melcery [SlotsPlusDictMeta]
;; The Meta Class:1 ends here

;; __init__


;; [[file:bakery.org::*__init__][__init__:1]]
(defn __init__ [cls #* args #** kwargs] (setv cls.m/stores [])))
;; __init__:1 ends here

;; The Milcery Class


;; [[file:bakery.org::*The Milcery Class][The Milcery Class:1]]
(defclass milcery [:metaclass melcery]
;; The Milcery Class:1 ends here



;; Adapted from [[the man himself][https://github.com/python/typing/issues/345#issuecomment-270814750]],
;; as well as from the [[https://github.com/cjrh/autoslot][autoslot]] documentation (by [[https://github.com/cjrh][Caleb Hattingh]]) [[https://github.com/cjrh/autoslot#weakref][here]]:


;; [[file:bakery.org::*The Milcery Class][The Milcery Class:2]]
(setv __slots__ [ "__weakref__" ])
;; The Milcery Class:2 ends here

;; Flatten Iterable

;; # TODO: Add to nanite


;; [[file:bakery.org::*Flatten Iterable][Flatten Iterable:1]]
#@(classmethod (defn cls/flatten [cls iterable [times None]]
                     (setv lst [])
                     (for [i iterable]
                          (if (and (coll? i)
                                   (or (is times None)
                                       times))
                              (.extend lst (.cls/flatten cls i :times (if times (dec times) times)))
                              (.append lst i)))
                     (return lst)))
;; Flatten Iterable:1 ends here

;; Split and Flatten


;; [[file:bakery.org::*Split and Flatten][Split and Flatten:1]]
#@(classmethod (defn cls/split-and-flatten [cls iterable] (.cls/flatten cls (gfor j (.cls/flatten cls iterable) (.split j)))))
;; Split and Flatten:1 ends here

;; Freezer


;; [[file:bakery.org::*Freezer][Freezer:1]]
#@(classmethod (defn cls/freezer [cls value freezer]
                      (cond [(not value) (setv freezer [])]
                            [(coll? value)
                             (do (if (not (isinstance freezer list)) (setv freezer []))
                                 (.extend freezer value)
                                 (setv freezer (.cls/flatten cls (gfor i freezer :if i i))))]
                            [True (raise (TypeError f"Sorry! The 'm/freezer' can only accept non-string iterables or non-truthy values!"))])
                      (return freezer)))
;; Freezer:1 ends here

;; String Prefix


;; [[file:bakery.org::*String Prefix][String Prefix:1]]
#@(classmethod (defn cls/string-prefix [cls b a] (+ a b)))
;; String Prefix:1 ends here

;; Process Attribute


;; [[file:bakery.org::*Process Attribute][Process Attribute:1]]
#@(classmethod (defn cls/process-attr [cls attr prefix]
                     (setv attr (unmangle attr))
                     (if (.startswith attr prefix)
                         (.replace attr "_" "-")
                         (-> attr
                             (.lstrip "_")
                             (.cls/string-prefix cls prefix)
                             (.replace "_" "-")
                             (mangle)))))
;; Process Attribute:1 ends here

;; Is Attribute


;; [[file:bakery.org::*Is Attribute][Is Attribute:1]]
#@(classmethod (defn cls/is-attr [cls attr]
                     (setv attr (unmangle attr))
                     (cond [(.endswith attr "__") (return "__")]
                           [(.startswith attr "__") (return "internal/")]
                           [(.startswith attr "_") (return "m/")]
                           [(.startswith attr "internal/") (return "internal/")]
                           [(.startswith attr "m/") (return "m/")]
                           [True (return False)])))
;; Is Attribute:1 ends here

;; Process If Attribute


;; [[file:bakery.org::*Process If Attribute][Process If Attribute:1]]
#@(classmethod (defn cls/process-if-attr [cls attr [return-bool False]]
                     (setv attr (unmangle attr))
                     (return (if (setx prefix (.cls/is-attr cls attr))
                                 (mangle (.cls/process-attr cls attr prefix))
                                 (if return-bool False (mangle attr))))))
;; Process If Attribute:1 ends here

;; Remove If Not Attribute


;; [[file:bakery.org::*Remove If Not Attribute][Remove If Not Attribute:1]]
#@(classmethod (defn cls/remove-if-not-attr [cls dct] (return (dfor [key value] (.items dct) :if (.cls/is-attr cls key) [ key value ]))))
;; Remove If Not Attribute:1 ends here

;; Trim Attribute Prefix


;; [[file:bakery.org::*Trim Attribute Prefix][Trim Attribute Prefix:1]]
#@(classmethod (defn cls/trim-attr-prefix [cls attr]
                     (setv attr (unmangle attr))
                     (let [prefix (.cls/is-attr cls attr)]
                          (return (, prefix (if prefix (mangle (.removeprefix attr prefix)) (mangle attr)))))))
;; Trim Attribute Prefix:1 ends here

;; Get Attribute


;; [[file:bakery.org::*Get Attribute][Get Attribute:1]]
#@(classmethod (defn cls/get-attr [cls dct attr [default False]]
                     (setv attr (unmangle attr))
                     (setv [prefix cls/get-attr/attr] (.cls/trim-attr-prefix cls attr))
                     (return (or (.get dct (mangle (+ "__" cls/get-attr/attr)) False)
                                 (.get dct (mangle (+ "_" cls/get-attr/attr)) False)
                                 (.get dct (mangle (+ "internal/" cls/get-attr/attr)) False)
                                 (.get dct (mangle (+ "m/" cls/get-attr/attr)) default)))))
;; Get Attribute:1 ends here

;; Freezer

;; This tells the bakery that the program is a combination of multiple programs, such as ~ls | tail~.


;; [[file:bakery.org::*Freezer][Freezer:1]]
#@(property (defn m/freezer [self] (return self.internal/freezer)))
#@(m/freezer.setter (defn m/freezer [self value] (setv self.internal/freezer (.cls/freezer self.__class__ value self.internal/freezer))))
;; Freezer:1 ends here

;; Return

;; Return the final command:


;; [[file:bakery.org::*Return][Return:1]]
#@(property (defn m/return-command [self] (return self.internal/return-command)))
#@(m/return-command.setter (defn m/return-command [self value]
                                 (setv self.internal/return-command (bool value))
                                 (if value (setv self.m/type str))))
;; Return:1 ends here

;; Print

;; Print the final command:


;; [[file:bakery.org::*Print][Print:1]]
#@(property (defn m/print-command [self] (return self.internal/print-command)))
#@(m/print-command.setter (defn m/print-command [self value]
                                (setv self.internal/print-command (bool value))
                                (if value (setv self.m/return-command True))))
;; Print:1 ends here

;; Run Interactively


;; [[file:bakery.org::*Run Interactively][Run Interactively:1]]
#@(property (defn m/run [self] (return (= self.m/capture "run"))))
#@(m/run.setter (defn m/run [self value] (if value (setv self.m/capture "run"))))
;; Run Interactively:1 ends here

;; Number of Lines

;; ~ordinal~ will shave off the first or last ~n~ lines off of ~std~, whether that be ~stdout~ or ~stderr~:


;; [[file:bakery.org::*Number of Lines][Number of Lines:1]]
#@(property (defn m/n-lines [self] (return self.internal/n-lines)))
#@(m/n-lines.setter (defn m/n-lines [self value]

    (setv ordinal (.get value "ordinal" "first"))
    (if ordinal
        (if (not (in ordinal (setx ordinals (, "first" "last"))))
            (raise (TypeError #[f[Sorry! You must choose an `ordinal' value from: {(.join ", " ordinals)}]f])))
        (assoc value "ordinal" "first"))

    (setv number (.get value "number" 0))
    (if number
        (cond [(is number None) None]
              [(< (int number) 1) (raise (ValueError "Sorry! `n' must be greater than 0!"))])
        (assoc value "number" None))

    (setv std (.get value "std" "stdout"))
    (if std
        (if (not (in std (setx stds (, "stdout" "stderr" "both"))))
            (raise (TypeError #[f[Sorry! You must choose an `std' value from: {(.join ", " stds)}]f]))
        (assoc value "std" "stdout")))
    
    (setv self.internal/n-lines (D value))))
;; Number of Lines:1 ends here

;; Context Manager

;; Use function as context manager:


;; [[file:bakery.org::*Context Manager][Context Manager:1]]
#@(property (defn m/c [self] (return self.m/context)))
#@(m/c.setter (defn m/c [self value] (setv self.m/context (bool value))))
;; Context Manager:1 ends here

;; Capture

;; Capture types, consisting of ~stdout~, ~stderr~, and both:


;; [[file:bakery.org::*Capture][Capture:1]]
#@(property (defn m/capture [self] (return self.internal/capture)))
#@(m/capture.setter (defn m/capture [self value]
                          (if (not (in value self.m/captures))
                              (raise (TypeError #[f[Sorry! Capture type "{value}" is not permitted! Choose from one of: {(.join ", " self.m/captures)}]f])))
                          (setv self.internal/capture value)))
;; Capture:1 ends here

;; Sudo


;; [[file:bakery.org::*Sudo][Sudo:1]]
#@(property (defn m/sudo [self] (return self.internal/sudo)))
#@(m/sudo.setter (defn m/sudo [self value]
                       (if (not (isinstance value self.m/type-groups.dict-like))
                           (raise (TypeError "Sorry! `m/sudo' needs to be a tea, frosting, or dict-like object!")))
                       (if (> (len value) 1)
                           (raise (ValueError "Sorry! The `m/sudo' object can only have a single key-value item!")))
                       (if (and value
                                (-> value (.keys) (iter) (next) (in (, "i" "s")) (not)))
                           (raise (ValueError "Sorry! The `m/sudo' object can only take `i' or `s' as a key!")))
                       (setv self.internal/sudo value)))
;; Sudo:1 ends here

;; __init__


;; [[file:bakery.org::*__init__][__init__:1]]
(defn __init__ [
        self
        #* args
        [program- None]
        [base-program- None]
        [freezer- None]
        #** kwargs]
;; __init__:1 ends here

;; Append bakery to list of bakeries

;; Adapted from [[https://stackoverflow.com/a/26626707/10827766][this answer]] by [[https://stackoverflow.com/users/100297/martijn-pieters][Martijn Pieters]], as well as [[https://stackoverflow.com/a/328882/10827766][this answer]] by [[https://stackoverflow.com/users/9567/torsten-marek][Torsten Marek]]:


;; [[file:bakery.org::*Append bakery to list of bakeries][Append bakery to list of bakeries:1]]
(.append self.__class__.m/stores (.ref weakref self self))
;; Append bakery to list of bakeries:1 ends here

;; Type Groups


;; [[file:bakery.org::*Type Groups][Type Groups:1]]
(setv self.m/type-groups (D {}))
;; Type Groups:1 ends here

;; Acceptable Arguments


;; [[file:bakery.org::*Acceptable Arguments][Acceptable Arguments:1]]
(setv self.m/type-groups.acceptable-args [str int])
;; Acceptable Arguments:1 ends here

;; Reprs


;; [[file:bakery.org::*Reprs][Reprs:1]]
(setv self.m/type-groups.reprs (, "str" "repr"))
;; Reprs:1 ends here

;; This Class and its Subclasses


;; [[file:bakery.org::*This Class and its Subclasses][This Class and its Subclasses:1]]
(setv self.m/type-groups.this-class-subclass [self.__class__])
(.extend self.m/type-groups.acceptable-args self.m/type-groups.this-class-subclass)
;; This Class and its Subclasses:1 ends here

;; Dict-Like


;; [[file:bakery.org::*Dict-Like][Dict-Like:1]]
(setv self.m/type-groups.dict-like [dict])
;; Dict-Like:1 ends here

;; Genstrings


;; [[file:bakery.org::*Genstrings][Genstrings:1]]
(setv self.m/type-groups.genstrings [tea frosting])
(.extend self.m/type-groups.acceptable-args self.m/type-groups.genstrings)
(.extend self.m/type-groups.acceptable-args self.m/type-groups.dict-like)
(setv self.m/type-groups.genstrings (tuple self.m/type-groups.genstrings))
;; Genstrings:1 ends here

;; Generators


;; [[file:bakery.org::*Generators][Generators:1]]
(setv self.m/type-groups.generators (, "generator" "iter" "chain" "tee"))
;; Generators:1 ends here

;; Excluded classes


;; [[file:bakery.org::*Excluded classes][Excluded classes:1]]
(setv self.m/type-groups.excluded-classes (, "type"))
;; Excluded classes:1 ends here

;; Post


;; [[file:bakery.org::*Post][Post:1]]
(setv self.m/type-groups.dict-like (tuple self.m/type-groups.dict-like))
;; Post:1 ends here



;; Note that only via ~baking~ can subcommand-specific arguments and keyword arguments be set.


;; [[file:bakery.org::*Subcommand][Subcommand:2]]
(setv self.m/subcommand (D {})
      self.m/subcommand.default "supercalifragilisticexpialidocious"
      self.m/subcommand.current (D {})
      self.m/subcommand.current.unprocessed "supercalifragilisticexpialidocious"
      self.m/subcommand.current.intact False
      self.m/subcommand.current.processed "supercalifragilisticexpialidocious")
;; Subcommand:2 ends here

;; Arguments


;; [[file:bakery.org::*Arguments][Arguments:1]]
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
;; Arguments:1 ends here

;; Keyword


;; [[file:bakery.org::*Keyword][Keyword:1]]
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
;; Keyword:1 ends here

;; Freezer


;; [[file:bakery.org::*Freezer][Freezer:1]]
(setv self.internal/freezer (.cls/freezer self.__class__ freezer- []))
;; Freezer:1 ends here

;; Program


;; [[file:bakery.org::*Program][Program:1]]
(setv self.m/program (or program- "")
      self.m/base-program (or base-program- program-))
;; Program:1 ends here

;; Return Categories


;; [[file:bakery.org::*Return Categories][Return Categories:1]]
(setv self.m/return-categories (,
    "stdout"
    "stderr"
    "return-codes"
    "command"
    "tea"
    "verbosity"
))
;; Return Categories:1 ends here

;; Command


;; [[file:bakery.org::*Command][Command:1]]
(setv self.m/command (tea))
;; Command:1 ends here

;; Settings


;; [[file:bakery.org::*Settings][Settings:1]]
(setv self.m/settings (D {})
      self.m/settings.defaults (D {})
      self.m/settings.current (D {}))
;; Settings:1 ends here

;; Gitea

;; Set ~m/gitea.bool~ to ~True~, or add the program to ~m/gitea.list~ to allow this program to do something like ~git(C = path).status()~,
;; and set ~m/gitea.off~ to override and disable both.

;; Named after [[https://gitea.io/en-us/][gitea]] and my own [[https://gitlab.com/picotech/nanotech/gensing][gensing]] modules:


;; [[file:bakery.org::*Gitea][Gitea:1]]
(setv self.m/gitea (D {})
      self.m/gitea.list [ "git" "yadm" ]
      self.m/gitea.bool (or (in self.m/program self.m/gitea.list) False)
      self.m/gitea.off False)
;; Gitea:1 ends here

;; Frozen Program

;; Return the bakery just before running the command; any type not in ~m/type-groups.acceptable-args~ will freeze the bakery:


;; [[file:bakery.org::*Frozen Program][Frozen Program:1]]
(setv self.m/frozen False)
(setv self.m/settings.defaults.m/frozen (deepcopy self.m/frozen))
;; Frozen Program:1 ends here

;; Capture Type

;; Which output stream to capture; values are listed below in ~m/captures~:


;; [[file:bakery.org::*Capture Type][Capture Type:1]]
(setv self.m/captures (, "stdout" "stderr" "both" "run"))
(setv self.internal/capture "stdout")
(setv self.m/settings.defaults.m/capture (deepcopy self.internal/capture))
;; Capture Type:1 ends here

;; Shell

;; What shell to use:


;; [[file:bakery.org::*Shell][Shell:1]]
(setv self.m/shell None)
(setv self.m/settings.defaults.m/shell (deepcopy self.m/shell))
;; Shell:1 ends here

;; Pretty Prining

;; Pretty print the output:


;; [[file:bakery.org::*Pretty Prining][Pretty Prining:1]]
(setv self.m/dazzle False)
(setv self.m/settings.defaults.m/dazzle (deepcopy self.m/dazzle))
;; Pretty Prining:1 ends here

;; Stdout

;; Ignore standard output:


;; [[file:bakery.org::*Stdout][Stdout:1]]
(setv self.m/ignore-stdout False)
(setv self.m/settings.defaults.m/ignore-stdout (deepcopy self.m/ignore-stdout))
;; Stdout:1 ends here

;; Stderr

;; Ignore standard error:


;; [[file:bakery.org::*Stderr][Stderr:1]]
(setv self.m/ignore-stderr False)
(setv self.m/settings.defaults.m/ignore-stderr (deepcopy self.m/ignore-stderr))
;; Stderr:1 ends here

;; Verbosity

;; How verbose the output should be:


;; [[file:bakery.org::*Verbosity][Verbosity:1]]
(setv self.m/verbosity 0)
(setv self.m/settings.defaults.m/verbosity (deepcopy self.m/verbosity))
;; Verbosity:1 ends here

;; Run As

;; Run bakery as program; useful when ~m/program~ is a path to a script:


;; [[file:bakery.org::*Run As][Run As:1]]
(setv self.m/run-as "")
(setv self.m/settings.defaults.m/run-as (deepcopy self.m/run-as))
;; Run As:1 ends here

;; Number of Lines

;; How many lines of output to return; can chop ~n~ lines off the top or bottom:


;; [[file:bakery.org::*Number of Lines][Number of Lines:1]]
(setv self.internal/n-lines (D { "ordinal" "first" "number" 0 "std" "stdout" }))
(setv self.m/settings.defaults.m/n-lines (deepcopy self.internal/n-lines))
;; Number of Lines:1 ends here

;; One Dash

;; Whether to use one dash for program options, such as in the case of ~find~:


;; [[file:bakery.org::*One Dash][One Dash:1]]
(setv self.m/one-dash False)
(setv self.m/settings.defaults.m/one-dash (deepcopy self.m/one-dash))
;; One Dash:1 ends here

;; Fixed

;; Whether to keep underscores in program options instead of replacing them with dashes:


;; [[file:bakery.org::*Fixed][Fixed:1]]
(setv self.m/fixed False)
(setv self.m/settings.defaults.m/fixed (deepcopy self.m/fixed))
;; Fixed:1 ends here

;; Intact Option

;; Whether to keep options as they are, not replacing underscores with dashes:


;; [[file:bakery.org::*Intact Option][Intact Option:1]]
(setv self.m/intact-option False)
(setv self.m/settings.defaults.m/intact-option (deepcopy self.m/intact-option))
;; Intact Option:1 ends here

;; Tiered

;; To use the ~m/tiered~ setting, bake the command in from before with all applicable
;; replacements replaced with ~{{ b.t }}~, and bake in ~m/tiered~ to True; then when
;; calling the command, pass in all the arguments that are going to replace the
;; ~{{ b.t }}~ previously baked into the command.

;; To reset the command function, use the ~splat-~ function as necessary.


;; [[file:bakery.org::*Tiered][Tiered:1]]
(setv self.m/tiered False)
(setv self.m/settings.defaults.m/tiered (deepcopy self.m/tiered))
;; Tiered:1 ends here

;; Input

;; Used to pass input to the ~subprocess Popen~ class; note that ~m/popen.stdin~ overrides this.


;; [[file:bakery.org::*Input][Input:1]]
(setv self.m/input None)
(setv self.m/settings.defaults.m/input (deepcopy self.m/input))
;; Input:1 ends here

;; Regular Args

;; An alternate way to pass arguments to the program as a separate list:


;; [[file:bakery.org::*Regular Args][Regular Args:1]]
(setv self.m/regular-args (,))
(setv self.m/settings.defaults.m/regular-args (deepcopy self.m/regular-args))
;; Regular Args:1 ends here

;; Regular Kwargs

;; An alternate way to pass options to the program as a separate dictionary:


;; [[file:bakery.org::*Regular Kwargs][Regular Kwargs:1]]
(setv self.m/regular-kwargs (D {}))
(setv self.m/settings.defaults.m/regular-kwargs (deepcopy self.m/regular-kwargs))
;; Regular Kwargs:1 ends here

;; Context Manager

;; Whether the bakery is being used with a context manager:


;; [[file:bakery.org::*Context Manager][Context Manager:1]]
(setv self.m/context False)
(setv self.m/settings.defaults.m/context (deepcopy self.m/context))
;; Context Manager:1 ends here

;; Return Command

;; Return the command itself instead of the output of the command.

;; A good way to debug commands is to see what the command actually was
;; use the ~m/return-command~ keyword argument to return the final command.


;; [[file:bakery.org::*Return Command][Return Command:1]]
(setv self.internal/return-command False)
(setv self.m/settings.defaults.m/return-command (deepcopy self.internal/return-command))
;; Return Command:1 ends here

;; Print Command

;; Print the returned command from the setting above.

;; A good way to debug commands is to see what the command actually was
;; use the ~m/print-command~ keyword argument to print the final command.


;; [[file:bakery.org::*Print Command][Print Command:1]]
(setv self.internal/print-command False)
(setv self.m/settings.defaults.m/print-command (deepcopy self.internal/print-command))
;; Print Command:1 ends here

;; Print Command and Run

;; Print the command and continue running.

;; A good way to debug commands is to see what the command actually was
;; use the ~m/print-command-and-run~ keyword argument to print the final command and continue running.


;; [[file:bakery.org::*Print Command and Run][Print Command and Run:1]]
(setv self.m/print-command-and-run False)
(setv self.m/settings.defaults.m/print-command-and-run (deepcopy self.m/print-command-and-run))
;; Print Command and Run:1 ends here

;; Type of Output

;; ~m/type~ can be any available type, such as:
;; - iter
;; - list
;; - tuple
;; - set
;; - frozenset


;; [[file:bakery.org::*Type of Output][Type of Output:1]]
(setv self.m/type iter)
(setv self.m/settings.defaults.m/type (deepcopy self.m/type))
;; Type of Output:1 ends here

;; Split Output By Whitespace

;; Split the output by newlines, tabs, spaces, etc.


;; [[file:bakery.org::*Split Output By Whitespace][Split Output By Whitespace:1]]
(setv self.m/split False)
(setv self.m/settings.defaults.m/split (deepcopy self.m/split))
;; Split Output By Whitespace:1 ends here

;; Use Single Forward Slash Instead of Dash

;; Use a single forward slash instead of a dash for options, as ~DOS~ expects:


;; [[file:bakery.org::*Use Single Forward Slash Instead of Dash][Use Single Forward Slash Instead of Dash:1]]
(setv self.m/dos False)
(setv self.m/settings.defaults.m/dos (deepcopy self.m/dos))
;; Use Single Forward Slash Instead of Dash:1 ends here

;; Wait

;; - If set to True, ~m/capture = "run"~ will wait for the process to finish before returning an addict dictionary of values depending on ~m/return~ and ~m/verbosity~
;; - If set to False, ~m/capture = "run"~ will return the ~Popen~ object
;; - If set to None, ~m/capture = "run"~ will wait for the process to finish before returning None


;; [[file:bakery.org::*Wait][Wait:1]]
(setv self.m/wait True)
(setv self.m/settings.defaults.m/wait (deepcopy self.m/wait))
;; Wait:1 ends here

;; Popen

;; A dictionary used to pass options to the ~subprocess Popen~ class:


;; [[file:bakery.org::*Popen][Popen:1]]
(setv self.m/popen (D {}))
(setv self.m/settings.defaults.m/popen (deepcopy self.m/popen))
;; Popen:1 ends here

;; Chunk Size

;; Chunk size used when reading with ~m/capture = "run"~:


;; [[file:bakery.org::*Chunk Size][Chunk Size:1]]
(setv self.m/chunk-size 512)
(setv self.m/settings.defaults.m/chunk-size (deepcopy self.m/chunk-size))
;; Chunk Size:1 ends here

;; Sudo

;; Dict must be in the form {"i" : user} or {"s" : user}, to use or not use the configuration files of the specified user:


;; [[file:bakery.org::*Sudo][Sudo:1]]
(setv self.internal/sudo (D {}))
(setv self.m/settings.defaults.m/sudo (deepcopy self.internal/sudo))
;; Sudo:1 ends here

;; Debug

;; Print all the current values after attempting to return the result of the command:


;; [[file:bakery.org::*Debug][Debug:1]]
(setv self.m/debug False)
(setv self.m/settings.defaults.m/debug (deepcopy self.m/debug))
;; Debug:1 ends here

;; End of Init


;; [[file:bakery.org::*End of Init][End of Init:1]]
)
;; End of Init:1 ends here

;; Magic String Output


;; [[file:bakery.org::*Magic String Output][Magic String Output:1]]
(defn misc/magic-string-output [self output]
      (return (if (not (.misc/type-name-is-string self :type/type (type output)))
                  "Sorry! The bakery is currently frozen, debugging, or has returned a Popen!"
                  output)))
;; Magic String Output:1 ends here

;; Recursive Unmangle


;; [[file:bakery.org::*Recursive Unmangle][Recursive Unmangle:1]]
(defn misc/recursive-unmangle [self dct]
      (return (D (dfor [key value]
                       (.items dct)
                       [(unmangle key)
                        (if (isinstance value dict)
                            (.misc/recursive-unmangle self value)
                            value)]))))
;; Recursive Unmangle:1 ends here

;; Type Name is String


;; [[file:bakery.org::*Type Name is String][Type Name is String:1]]
(defn misc/type-name-is-string [self [type/type None]]
      (return (in (. (or type/type self.m/type) __name__) self.m/type-groups.reprs)))
;; Type Name is String:1 ends here

;; Return None if Type Name is String


;; [[file:bakery.org::*Return None if Type Name is String][Return None if Type Name is String:1]]
(defn misc/return-none-if-tnis [self [type/type None]]
      (return (if (.misc/type-name-is-string self :type/type type/type) "None" None)))
;; Return None if Type Name is String:1 ends here

;; Reset All


;; [[file:bakery.org::*Reset All][Reset All:1]]
(defn m/reset-all [self]
      (.reset- self)
      (.command/reset self))
;; Reset All:1 ends here

;; Generator


;; [[file:bakery.org::*Generator][Generator:1]]
(defn convert/generator [self input] (yield-from input))
;; Generator:1 ends here

;; Type


;; [[file:bakery.org::*Type][Type:1]]
(defn convert/type [self input [type/type None]]
    (setv type/type/type (or type/type self.m/type))
    (if (is input None) (return (.misc/return-none-if-tnis self :type/type type/type/type)))
    (if (and input (isinstance input frosting))
        (let [frosted-input (input)]
             (cond [(isinstance frosted-input str)
                    (setv input [(.fill (TextWrapper :break-long-words False :break-on-hyphens False) frosted-input)])]
                   [(is frosted-input None) (return (.misc/return-none-if-tnis self :type/type type/type/type))]
                   [(isinstance frosted-input int) (if (.misc/type-name-is-string self :type/type type/type/type)
                                                       (return (pretty-repr frosted-input))
                                                       (return frosted-input))])))
    (cond [(.misc/type-name-is-string self :type/type type/type/type) (return (.join "\n" input))]
          [(in type/type/type.__name__ self.m/type-groups.generators) (return (.convert/generator self input))]
          [True (return (type/type/type input))]))
;; Type:1 ends here

;; Get


;; [[file:bakery.org::*Get][Get:1]]
(defn subcommand/get [self #** kwargs]
      (setv self.m/subcommand.current.intact (.cls/get-attr self.__class__ kwargs "m/intact-subcommand"))
      (setv subcommand (.cls/get-attr self.__class__ kwargs "m/subcommand" :default self.m/subcommand.default))
      (if (!= subcommand self.m/subcommand.default)
          (setv self.m/subcommand.current.unprocessed subcommand)))
;; Get:1 ends here

;; Process


;; [[file:bakery.org::*Process][Process:1]]
(defn subcommand/process [self]
    (setv self.m/subcommand.current.processed (if self.m/subcommand.current.intact
                                                  self.m/subcommand.current.unprocessed
                                                  (unmangle (.replace self.m/subcommand.current.unprocessed "_" "-")))))
;; Process:1 ends here

;; Set Defaults


;; [[file:bakery.org::*Set Defaults][Set Defaults:1]]
(defn var/set-defaults [self]
      (for [[key value] (.items self.m/settings.defaults)]
           (setattr self key (deepcopy value))))
;; Set Defaults:1 ends here

;; Setup


;; [[file:bakery.org::*Setup][Setup:1]]
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

    (setv self.m/args.called args)
    (setv self.m/kwargs.called kwargs)

    (.var/process-all self #* args #** kwargs)

    (.var/apply self))
;; Setup:1 ends here

;; Reset

;; Note that ~subcommand~ is only really needed here to help reset the baked arguments and keyword arguments.


;; [[file:bakery.org::*Reset][Reset:1]]
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
;; Reset:1 ends here

;; Process


;; [[file:bakery.org::*Process][Process:1]]
(defn var/process-all [self #* args #** kwargs]
      (.var/process-args self #* self.m/args.world)
      (.var/process-args self #* self.m/args.instantiated)
      (.var/process-args self #* (. self m/args baked [self.m/subcommand.current.unprocessed]))
      (.var/process-args self #* args)

      (.var/process-kwargs self #** self.m/kwargs.world)
      (.var/process-kwargs self #** self.m/kwargs.instantiated)
      (.var/process-kwargs self #** (. self m/kwargs baked [self.m/subcommand.current.unprocessed]))
      (.var/process-kwargs self #** kwargs))
;; Process:1 ends here

;; Arguments


;; [[file:bakery.org::*Arguments][Arguments:1]]
(defn var/process-args [self #* args [starter False]]
      (for [arg args]
           (if (isinstance arg (tuple self.m/type-groups.acceptable-args))
               (if (isinstance (. self m/args current unprocessed [(if starter "starter" "regular")]) list)
                   (.append (. self m/args current unprocessed [(if starter "starter" "regular")]) arg)
                   (assoc self.m/args.current.unprocessed (if starter "starter" "regular") [arg]))
               (do (setv self.m/settings.current.m/frozen True)))))
;; Arguments:1 ends here

;; Keyword Arguments


;; [[file:bakery.org::*Keyword Arguments][Keyword Arguments:1]]
(defn var/process-kwargs [self #** kwargs]
      (defn inner [itr [starter False]]
            (for [[key value] (.items itr)]
                 (if (setx var/process/key-prefix (.cls/is-attr self.__class__ key))
                     (let [var/process/key (.cls/process-attr self.__class__ key var/process/key-prefix)]
                          (cond [(= var/process/key "m/starter-args")
                                 (.var/process-args self #* (if (isinstance value str) (, value) value) :starter True)]
                                [(= var/process/key "m/starter-kwargs") (inner value :starter True)]
;; Keyword Arguments:1 ends here



;; The values in ~m/regular-args~ will always be appended to ~self.m/args.current.regular~,
;; since ~m/regular-args~ is a keyword argument.


;; [[file:bakery.org::*Keyword Arguments][Keyword Arguments:2]]
[(= var/process/key "m/regular-args") (.var/process-args self #* value)]
;; Keyword Arguments:2 ends here



;; Note that, depending on where ~m/regular-kwargs~ is in the keyword arguments of the function call,
;; its values will replace any prexisting values of the same type; for example, in the following case,
;; where ~m/frozen~ is True, while ~m/regular-kwargs.frozen~ is False:
;; - If ~m/regular-kwargs~ is before ~m/frozen~, the value of ~m/frozen~ will replace the value of ~m/regular-kwargs.frozen~, and final value of ~m/frozen~ will be True
;; - If ~m/regular-kwargs~ is after ~m/frozen~, the value of ~m/regular-kwargs.frozen~ will replace the value of ~m/frozen~, and final value of ~m/frozen~ will be False
;; In other words, the values of whichever comes first will be replaced by the value of whichever comes second.


;; [[file:bakery.org::*Keyword Arguments][Keyword Arguments:3]]
[(= var/process/key "m/regular-kwargs") (inner value)]
;; Keyword Arguments:3 ends here



;; Adapted from [[https://stackoverflow.com/users/2988730/mad-physicist][Mad Physicist's]] answer [[https://stackoverflow.com/a/70794425/10827766][here]]:


;; [[file:bakery.org::*Keyword Arguments][Keyword Arguments:4]]
[(let [trimmed-attr (-> self.__class__ (.cls/trim-attr-prefix var/process/key) (get 1))]
      (and (not (in trimmed-attr self.m/type-groups.excluded-classes))
           (class? (setx literal-attr (.get (globals) trimmed-attr (getattr builtins trimmed-attr None))))
           value))
 (setv self.m/settings.current.m/type literal-attr)]
;; Keyword Arguments:4 ends here

;; [[file:bakery.org::*Keyword Arguments][Keyword Arguments:5]]
[True (if (not (in var/process/key (, "m/subcommand")))
                                    (assoc self.m/settings.current key value))]))
               (assoc (. self m/kwargs current unprocessed [(if starter "starter" "regular")]) key value))))
(inner kwargs))
;; Keyword Arguments:5 ends here

;; Apply


;; [[file:bakery.org::*Apply][Apply:1]]
(defn var/apply [self]
    (for [[key value] (.items self.m/settings.current)]
         (setattr self key value)))
;; Apply:1 ends here

;; Reset


;; [[file:bakery.org::*Reset][Reset:1]]
(defn command/reset [self]
      (if (not self.m/frozen)
          (setv self.m/command (tea))))
;; Reset:1 ends here

;; Process


;; [[file:bakery.org::*Process][Process:1]]
(defn command/process-all [self]
      (for [i (range 2)]
           (.command/process-args self :starter i)
           (.command/process-kwargs self :starter i)))
;; Process:1 ends here

;; Arguments


;; [[file:bakery.org::*Arguments][Arguments:1]]
(defn command/process-args [self [starter False]]
      (for [arg (. self m/args current unprocessed [(if starter "starter" "regular")])]
           (setv command/process-args/arg (cond [(isinstance arg self.m/type-groups.genstrings) (arg)]
                                                [(isinstance arg int) (str arg)]
                                                [(isinstance arg self.__class__) (arg :m/type str)]
                                                [True arg]))
           (if (isinstance (. self m/args current processed [(if starter "starter" "regular")]) list)
               (.append (. self m/args current processed [(if starter "starter" "regular")]) command/process-args/arg)
               (assoc self.m/args.current.processed (if starter "starter" "regular") [command/process-args/arg]))))
;; Arguments:1 ends here

;; Keyword Arguments

;; If the boolean value is non-truthy, don't put the argument in;
;; for example, if "program.subcommand([...], option = False)", then the result would be "program subcommand [...]",
;; i.e. without "--option".


;; [[file:bakery.org::*Keyword Arguments][Keyword Arguments:1]]
(defn command/process-kwargs [self [starter False]]
      (defn inner [value]
            (setv new-value (cond [(isinstance value self.m/type-groups.genstrings) (value)]
;; Keyword Arguments:1 ends here



;; Be very careful here; since ~bool~ is a subclass of ~int~, we need to first check if ~value~ is an instance of ~bool~, then ~int~,
;; otherwise ~(isinstance value int)~ will catch both cases.


;; [[file:bakery.org::*Keyword Arguments][Keyword Arguments:2]]
[(isinstance value bool) None]
[(isinstance value int) (str value)]
;; Keyword Arguments:2 ends here

;; [[file:bakery.org::*Keyword Arguments][Keyword Arguments:3]]
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
                                                                              (.replace key "_" "-"))
                                               command/process-kwargs/key (cond [(or (= k "dos")
                                                                                     self.m/dos)
                                                                                 (+ "/" command/process-kwargs/key)]
                                                                                [(or (= k "one-dash")
                                                                                     self.m/one-dash
                                                                                     (= (len command/process-kwargs/key) 1))
                                                                                 (+ "-" command/process-kwargs/key)]
                                                                                [True (+ "--" command/process-kwargs/key)])
                                               command/process-kwargs/key-values (cond [(= k "repeat") (lfor i (range (inc v)) command/process-kwargs/key)]
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
                                    command/process-kwargs/key (if self.m/fixed key (.replace key "_" "-"))
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
;; Keyword Arguments:3 ends here

;; Create Command


;; [[file:bakery.org::*Create Command][Create Command:1]]
(defn command/create [self]
      (if self.m/sudo
          (.append self.m/command
                   f"sudo -{(-> self.m/sudo (.keys) (iter) (next))} -u {(-> self.m/sudo (.values) (iter) (next))}"))

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
;; Create Command:1 ends here

;; Return


;; [[file:bakery.org::*Return][Return:1]]
(defn return/output [self]
      (cond [self.m/frozen (return (deepcopy self))]
            [self.m/return-command (return (.m/command self))]
            [True (let [output (.return/process self)]
                       (if (isinstance output dict)
                           (do (setv [peek-value output.stderr] (peek output.stderr :return-first 2)
                                     stds (, "out" "err"))
                               (if (and peek-value
                                        (not self.m/ignore-stderr))
                                   (raise (SystemError (+ f"In trying to run {(.m/command self)}:\n\n" (.join "\n" output.stderr)))))
                               (for [[std opp] (zip stds (py "stds[::-1]"))]
                                    (setv stdstd (+ "std" std)
                                          stdopp (+ "std" opp))
                                    (if (< self.m/verbosity 1)
                                        (if (= self.m/capture stdstd)
                                            (del (get output stdopp)))))))
                       (return output))]))
;; Return:1 ends here

;; Process


;; [[file:bakery.org::*Process][Process:1]]
(defn return/process [self]
    (if (.m/command self)
        (do (setv process (.m/popen-partial self))
            (cond [(is self.m/wait None) (with [p (process :pp-stdout DEVNULL :pp-stderr DEVNULL)]
                                               (return (.misc/return-none-if-tnis self)))]
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
                                     (if (not (and (is self.m/n-lines.number None)
                                                   (.misc/type-name-is-string self)))
                                         (let [trim-part (partial trim :ordinal self.m/n-lines.ordinal
                                                                       :number self.m/n-lines.number

                                                                       ;; TODO: After converting `nanite' / `nanotech' to `hy', change this to `type-'
                                                                       :_type self.m/type

                                                                       :ignore-check True)]
                                              (if (in self.m/n-lines.std (, "stdout" "both"))
                                                  (setv return/process/return.stdout (trim-part :iterable return/process/return.stdout)))
                                              (if (in self.m/n-lines.std (, "stderr" "both"))
                                                  (setv return/process/return.stderr (trim-part :iterable return/process/return.stderr)))))
                                     (return return/process/return))]
                  [True (return (process))]))
        (return (.misc/return-none-if-tnis self))))
;; Process:1 ends here

;; Frosting


;; [[file:bakery.org::*Frosting][Frosting:1]]
(defn return/frosting [self]
      (setv output (.return/output self)
            frosted-output (if (and (isinstance output self.m/type-groups.dict-like)
                                    (= (len output) 1))
                               (-> output (.values) (iter) (next))
                               output)
            dict-like-frosted-output (isinstance frosted-output self.m/type-groups.dict-like)
            frosted-output (if self.m/dazzle
                               (cond [dict-like-frosted-output frosted-output]
                                     [(coll? frosted-output) (list frosted-output)]
                                     [True [frosted-output]])
                               frosted-output))
      (if self.m/print-command-and-run (print (.m/command self)))
      (cond [(or self.m/frozen (= self.m/wait False)) (return frosted-output)]
            [self.m/print-command (print frosted-output)]
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
                      (let [new-frosted-output (get frosted-output stdstd)]
                           (if self.m/split
                               (setv new-frosted-output (.cls/split-and-flatten self.__class__ new-frosted-output)))
                           (assoc frosted-output stdstd (.convert/type self new-frosted-output))))
                  (else (return new-frosted-output)))]
            [(is self.m/wait None) (return (.misc/return-none-if-tnis self))]
            [True (let [new-frosted-output (frosting frosted-output self.m/capture)]
                       (if self.m/split
                           (setv new-frosted-output (.cls/split-and-flatten self.__class__ new-frosted-output)))
                       (return (.convert/type self new-frosted-output)))]))
;; Frosting:1 ends here

;; Popen Partial


;; [[file:bakery.org::*Popen Partial][Popen Partial:1]]
(defn m/popen-partial [self [stdout None] [stderr None]]
      (setv pp-stdout (cond [stdout]
                            [(= self.m/capture "stderr") (.get self.m/popen "stdout" DEVNULL)]
                            [(= self.m/capture "run") (.get self.m/popen "stdout" None)]
                            [True (if self.m/ignore-stdout
                                      (.get self.m/popen "stdout" DEVNULL)
                                      (.get self.m/popen "stdout" PIPE))])
            pp-stderr (or stderr (if (= self.m/capture "run")
                          (.get self.m/popen "stderr" None)
                          (if self.m/ignore-stderr
                              (.get self.m/popen "stderr" DEVNULL)
                              (.get self.m/popen "stderr" PIPE))))
            bufsize (.get self.m/popen "bufsize" -1)
            universal-newlines (.get self.m/popen "universal-newlines" None)
            universal-text (if (= bufsize 1)
                               True
                               universal-newlines)
            shell (.get self.m/popen "shell" (bool self.m/freezer))
            command (.m/command self)
            executable (if (setx exe (.get self.m/popen "executable" None)) (fullpath exe) exe))
      (return (partial Popen
                       (if self.m/freezer
                           command
                           (if shell
                               (join (split command))
                               (split command)))
                       :bufsize bufsize
                       :stdin (.get self.m/popen "stdin" self.m/input)
                       :stdout pp-stdout
                       :stderr pp-stderr
                       :executable executable
                       :universal-newlines universal-text
                       :text universal-text
                       :shell shell
                       #** self.m/popen)))
;; Popen Partial:1 ends here

;; Run


;; [[file:bakery.org::*Run][Run:1]]
(defn m/spin [self #* args [subcommand- "supercalifragilisticexpialidocious"] #** kwargs]
      (try (.var/setup self #* args :subcommand- subcommand- #** kwargs)
           (.command/process-all self)
           (.command/create self)
           (return (.return/frosting self))
           (finally (if self.m/debug (.inspect- self))
                    (.m/reset-all self))))
;; Run:1 ends here

;; Apply Pipe or Redirect


;; [[file:bakery.org::*Apply Pipe or Redirect][Apply Pipe or Redirect:1]]
(defn m/apply-pipe-redirect [self pr value]
    (setv is-milcery (isinstance value self.__class__))
    (defn inner [v]
          (let [type-string (.join ", " (gfor t (+ (list self.m/type-groups.genstrings)
                                                   self.m/type-groups.this-class-subclass
                                                   [str]) t.__name__))]
               (return (cond [(isinstance v self.m/type-groups.genstrings) [(v)]]
                             [is-milcery (or v.m/freezer (.values v.m/command) [v.m/program])]
                             [(isinstance v str) [v]]
                             [True (raise (NotImplemented f"Sorry! Value '{v}' can only be of the following types: {type-string}"))]))))
;; Apply Pipe or Redirect:1 ends here



;; If the value is a tuple, assume the first item is the value itself, while the second item is the pr;
;; this allows for more compilcated redirects, such as ~&>~, ~2>&1~, etc.


;; [[file:bakery.org::*Apply Pipe or Redirect][Apply Pipe or Redirect:2]]
(if (isinstance value tuple)
    (if (= (len value) 2)
        (setv processed-value (inner (first value))
              processed-pr (get value 1))
        (raise (NotImplemented "Sorry! A tuple value may only contain 2 items: (value, pr)")))
    (setv processed-value (inner value)
          processed-pr pr))
;; Apply Pipe or Redirect:2 ends here

;; [[file:bakery.org::*Apply Pipe or Redirect][Apply Pipe or Redirect:3]]
(setv kwargs {}
      base-program- (or self.m/base-program self.m/program)
;; Apply Pipe or Redirect:3 ends here



;; Note that ~freezer-~ will always use the ~m/freezer~ value from the bakery on the left-hand side of the operation calling it:


;; [[file:bakery.org::*Apply Pipe or Redirect][Apply Pipe or Redirect:4]]
freezer- (+ (or self.m/freezer (.values self.m/command) [self.m/program]) [processed-pr processed-value]))
;; Apply Pipe or Redirect:4 ends here

;; [[file:bakery.org::*Apply Pipe or Redirect][Apply Pipe or Redirect:5]]
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
                         :base-program- base-program-
                         #** kwargs)))
;; Apply Pipe or Redirect:5 ends here

;; Miscellaneous


;; [[file:bakery.org::*Miscellaneous][Miscellaneous:1]]
(defn deepcopy- [self #* args [subcommand- "supercalifragilisticexpialidocious"] #** kwargs]
      (setv cls (deepcopy self))
      (.bake- cls #* args :instantiated- True :m/subcommand subcommand- #** kwargs)
      (return cls))
;; Miscellaneous:1 ends here

;; Freeze


;; [[file:bakery.org::*Freeze][Freeze:1]]
(defn freeze- [self] (setv self.m/frozen True))
;; Freeze:1 ends here

;; Defrost


;; [[file:bakery.org::*Defrost][Defrost:1]]
(defn defrost- [self] (setv self.m/frozen self.m/settings.m/frozen))
;; Defrost:1 ends here

;; Great [Insert Country Here] Bakeoff!

;; [["Bake"][https://amoffat.github.io/sh/sections/baking.html]] arguments and options into the command from before for specific subcommands:


;; [[file:bakery.org::*Great \[Insert Country Here\] Bakeoff!][Great [Insert Country Here] Bakeoff!:1]]
(defn bake- [self #* args [subcommand- "supercalifragilisticexpialidocious"] [instantiated- False] #** kwargs ]
      (.extend (if instantiated-
                   self.m/args.instantiated
                   (. self m/args baked [subcommand-])) args)
      (.update (if instantiated-
                   self.m/kwargs.instantiated
                   (. self m/kwargs baked [subcommand-])) kwargs))
;; Great [Insert Country Here] Bakeoff!:1 ends here

;; Bake All

;; [["Bake"][https://amoffat.github.io/sh/sections/baking.html]] arguments and options into all bakeries:


;; [[file:bakery.org::*Bake All][Bake All:1]]
(defn bake-all- [self #* args #** kwargs ]
      (for [store (.chain- self)]
           (.extend store.m/args.world args)
           (.update store.m/kwargs.world kwargs)))
;; Bake All:1 ends here

;; Unbake

;; Remove baked arguments and options; accepts keyword arguments taken by ~reset-~:


;; [[file:bakery.org::*Unbake][Unbake:1]]
(defn splat- [self [set-defaults False] #** kwargs] (.reset- self :baked True :set-defaults set-defaults))
;; Unbake:1 ends here

;; Unbake All

;; Remove arguments and options from all bakeries; accepts keyword arguments taken by ~reset-~:


;; [[file:bakery.org::*Unbake All][Unbake All:1]]
(defn splat-all- [self [set-defaults False] #** kwargs]
      (for [store (.chain- self)]
           (.reset- self :set-defaults set-defaults #** kwargs)))
;; Unbake All:1 ends here

;; Current Values

;; Return an ~addict~ dictionary with all the current values for the class variables;
;; can be used for debugging purposes or otherwise.


;; [[file:bakery.org::*Current Values][Current Values:1]]
(defn current-values- [self]
      (return (D { "__slots__" (.misc/recursive-unmangle self (dfor var
                                                                    self.__slots__
                                                                    :if (!= var "__dict__")
                                                                    [var (getattr self var)]))
                   "__dict__" self.__dict__ })))
;; Current Values:1 ends here

;; Print

;; Debug the current function:


;; [[file:bakery.org::*Print][Print:1]]
(defn inspect- [self #** kwargs] 
      (if (not kwargs)
          (setv kwargs { "all" True }))
      (inspect self #** kwargs))
;; Print:1 ends here

;; Original

;; Get the original bakery object:


;; [[file:bakery.org::*Original][Original:1]]
(defn origin- [self] (return (. (first self.__class__.m/stores) __callback__)))
;; Original:1 ends here

;; All

;; Return a list of all bakeries:


;; [[file:bakery.org::*All][All:1]]
(defn chain- [self] (return (lfor store self.__class__.m/stores store.__callback__)))
;; All:1 ends here

;; __call__


;; [[file:bakery.org::*__call__][__call__:1]]
(defn __call__ [
        self
        #* args
        [args-before-func (,)]
        #** kwargs ]
    (if (and (not self.m/gitea.off)
             (or self.m/gitea.bool
                 (in self.m/program self.m/gitea.list)))
        (return (.deepcopy- self :m/starter-args args :m/starter-kwargs kwargs))
        (cond [(or (.cls/get-attr self.__class__ kwargs "m/context" False)
                   (.cls/get-attr self.__class__ kwargs "m/c" False))
               (return (.deepcopy- self #* args  #** kwargs))]
              [True (return (.m/spin self #* args  #** kwargs))])))
;; __call__:1 ends here

;; __setattr__


;; [[file:bakery.org::*__setattr__][__setattr__:1]]
(defn __setattr__ [self attr value] (.__setattr__ (super) (.cls/process-if-attr self.__class__ attr) value))
;; __setattr__:1 ends here

;; __getattr__


;; [[file:bakery.org::*__getattr__][__getattr__:1]]
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
;; __getattr__:1 ends here

;; __copy__

;; Note that copies have ~m/frozen~ set to its default.

;; Adapted from [[https://gist.github.com/shadowrylander/a4d861fc37d381b8edc4b8e7793000d1][here]]:


;; [[file:bakery.org::*__copy__][__copy__:1]]
(defn __copy__ [self]
;; __copy__:1 ends here



;; #+begin_quote
;; Create a new instance
;; #+end_quote


;; [[file:bakery.org::*__copy__][__copy__:2]]
(setv cls self.__class__
      result (.__new__ cls cls)
;; __copy__:2 ends here



;; #+begin_quote
;; Get all ~__slots__~ of the derived class
;; #+end_quote


;; [[file:bakery.org::*__copy__][__copy__:3]]
slots (.from-iterable chain (lfor s self.__class__.__mro__ (getattr s "__slots__" []))))
;; __copy__:3 ends here



;; #+begin_quote
;; Copy all attributes
;; #+end_quote


;; [[file:bakery.org::*__copy__][__copy__:4]]
(for [var slots] (if (not (in var (, "__weakref__"))) (setattr result var (copy (getattr self var)))))
(.update result.__dict__ self.__dict__)
;; __copy__:4 ends here



;; Reset ~m/frozen~:


;; [[file:bakery.org::*__copy__][__copy__:5]]
(setv result.m/frozen result.m/settings.defaults.m/frozen)
;; __copy__:5 ends here



;; #+begin_quote
;; Return updated instance
;; #+end_quote


;; [[file:bakery.org::*__copy__][__copy__:6]]
(return result))
;; __copy__:6 ends here

;; __deepcopy__

;; Note that deepcopies have ~m/frozen~ set to its default.

;; Adapted from [[https://gist.github.com/shadowrylander/a4d861fc37d381b8edc4b8e7793000d1][here]]:


;; [[file:bakery.org::*__deepcopy__][__deepcopy__:1]]
(defn __deepcopy__ [self memo]
;; __deepcopy__:1 ends here



;; #+begin_quote
;; Create a new instance
;; #+end_quote


;; [[file:bakery.org::*__deepcopy__][__deepcopy__:2]]
(setv cls self.__class__
      result (.__new__ cls cls))
;; __deepcopy__:2 ends here



;; #+begin_quote
;; Don't copy self reference
;; #+end_quote


;; [[file:bakery.org::*__deepcopy__][__deepcopy__:3]]
(assoc memo (id self) result)
;; __deepcopy__:3 ends here



;; #+begin_quote
;; Don't copy the cache - if it exists
;; #+end_quote


;; [[file:bakery.org::*__deepcopy__][__deepcopy__:4]]
(if (and (hasattr self "m/cache") self.m/cache) (assoc memo (id self.m/cache) (.__new__ self.m/cache dict)))
;; __deepcopy__:4 ends here



;; #+begin_quote
;; Get all ~__slots__~ of the derived class
;; #+end_quote


;; [[file:bakery.org::*__deepcopy__][__deepcopy__:5]]
(setv slots (.from-iterable chain (lfor s self.__class__.__mro__ (getattr s "__slots__" []))))
;; __deepcopy__:5 ends here



;; #+begin_quote
;; Deep copy all other attributes
;; #+end_quote


;; [[file:bakery.org::*__deepcopy__][__deepcopy__:6]]
(for [var slots] (if (not (in var (, "__weakref__"))) (setattr result var (deepcopy (getattr self var) memo))))
(for [[k v] (.items self.__dict__)] (setattr result k (deepcopy v memo)))
;; __deepcopy__:6 ends here



;; Reset ~m/frozen~:


;; [[file:bakery.org::*__deepcopy__][__deepcopy__:7]]
(setv result.m/frozen result.m/settings.defaults.m/frozen)
;; __deepcopy__:7 ends here



;; #+begin_quote
;; Return updated instance
;; #+end_quote


;; [[file:bakery.org::*__deepcopy__][__deepcopy__:8]]
(return result))
;; __deepcopy__:8 ends here

;; __iter__


;; [[file:bakery.org::*__iter__][__iter__:1]]
(defn __iter__ [self]
    (setv self.m/n 0
          self.m/output (.m/spin self))
    (return self))
;; __iter__:1 ends here

;; __next__


;; [[file:bakery.org::*__next__][__next__:1]]
(defn __next__ [self]
      (try (setv output-len (len self.m/output))
           (except [TypeError]
                   (return (next self.m/output)))
           (else (hyrulem/n output-len)
                     (do (+= self.m/n 1)
                         (return (get self.m/output (dec self.m/n))))
                     (raise StopIteration))))
;; __next__:1 ends here

;; __str__

;; If ~__str__~ doesn't exist, ~__repr__~ called by ~(inspect self)~ trigger in infinite loop when getting the title of the report.


;; [[file:bakery.org::*__str__][__str__:1]]
(defn __str__ [self] (return (or (.m/command self) f"<{self.__class__.__module__}.{self.__class__.__name__} object at {(hex (id self))}>")))
;; __str__:1 ends here

;; __repr__

;; If ~__str__~ doesn't exist, ~__repr__~ called by ~(inspect self)~ trigger in infinite loop when getting the title of the report.


;; [[file:bakery.org::*__repr__][__repr__:1]]
(defn __repr__ [self] (.inspect- self) (return (str self)))
;; __repr__:1 ends here

;; __or__


;; [[file:bakery.org::*__or__][__or__:1]]
(defn __or__ [self value] (return (.m/apply-pipe-redirect self "|" value)))
;; __or__:1 ends here

;; __and__


;; [[file:bakery.org::*__and__][__and__:1]]
(defn __and__ [self value] (return (.m/apply-pipe-redirect self "| tee" value)))
;; __and__:1 ends here

;; __add__


;; [[file:bakery.org::*__add__][__add__:1]]
(defn __add__ [self value] (return (.m/apply-pipe-redirect self "| tee -a" value)))
;; __add__:1 ends here

;; __lt__


;; [[file:bakery.org::*__lt__][__lt__:1]]
(defn __lt__ [self value] (return (.m/apply-pipe-redirect self "<" value)))
;; __lt__:1 ends here

;; __lshift__


;; [[file:bakery.org::*__lshift__][__lshift__:1]]
(defn __lshift__ [self value] (return (.m/apply-pipe-redirect self "<<" value)))
;; __lshift__:1 ends here

;; __gt__


;; [[file:bakery.org::*__gt__][__gt__:1]]
(defn __gt__ [self value] (return (.m/apply-pipe-redirect self ">" value)))
;; __gt__:1 ends here

;; __rshift__


;; [[file:bakery.org::*__rshift__][__rshift__:1]]
(defn __rshift__ [self value] (return (.m/apply-pipe-redirect self ">>" value)))
;; __rshift__:1 ends here

;; __ror__


;; [[file:bakery.org::*__ror__][__ror__:1]]
(defn __or__ [self value] (return (.m/apply-pipe-redirect self "|" value)))
;; __ror__:1 ends here

;; __rand__


;; [[file:bakery.org::*__rand__][__rand__:1]]
(defn __and__ [self value] (return (.m/apply-pipe-redirect self "| tee" value)))
;; __rand__:1 ends here

;; __radd__


;; [[file:bakery.org::*__radd__][__radd__:1]]
(defn __add__ [self value] (return (.m/apply-pipe-redirect self "| tee -a" value)))
;; __radd__:1 ends here

;; __rlt__


;; [[file:bakery.org::*__rlt__][__rlt__:1]]
(defn __lt__ [self value] (return (.m/apply-pipe-redirect self "<" value)))
;; __rlt__:1 ends here

;; __rlshift__


;; [[file:bakery.org::*__rlshift__][__rlshift__:1]]
(defn __lshift__ [self value] (return (.m/apply-pipe-redirect self "<<" value)))
;; __rlshift__:1 ends here

;; __rgt__


;; [[file:bakery.org::*__rgt__][__rgt__:1]]
(defn __gt__ [self value] (return (.m/apply-pipe-redirect self ">" value)))
;; __rgt__:1 ends here

;; __rrshift__


;; [[file:bakery.org::*__rrshift__][__rrshift__:1]]
(defn __rshift__ [self value] (return (.m/apply-pipe-redirect self ">>" value)))
;; __rrshift__:1 ends here

;; __enter__


;; [[file:bakery.org::*__enter__][__enter__:1]]
(defn __enter__ [self] (return (deepcopy self)))
;; __enter__:1 ends here

;; __exit__


;; [[file:bakery.org::*__exit__][__exit__:1]]
(defn __exit__ [self exception-type exception-val exception-traceback] False)
;; __exit__:1 ends here

;; End of Milcery


;; [[file:bakery.org::*End of Milcery][End of Milcery:1]]
)
;; End of Milcery:1 ends here
