#!/usr/bin/env mdsh
# bakery

***

### Running [mdsh](https://github.com/bashup/mdsh), by [bashup](https://github.com/bashup)

If you have `mdsh`, you can run this README on your own machine after you've installed the module! Note, however, that the code blocks completely greyed out will not be run, as they are case-specific.
```bash !
sudo chmod +x README.md
./README.md
```

`Note:` The following is to initialize the python3.8 processor for `mdsh`; *the above is the command to run this README!*
```bash @mdsh
mdsh-lang-python() { /usr/bin/env python3.8; }
```

***

## Welcome to the `bakery`! May I wrap your program?

&nbsp;&nbsp;&nbsp;&nbsp; `bakery` is a python module heavily inspired by [`sh`](https://amoffat.github.io/sh/), written by [`Andrew Moffat / amoffat`](https://github.com/amoffat); I loved the concept of `baking` a command so much that I created an entire module based on it.

&nbsp;&nbsp;&nbsp;&nbsp; While amoffat's `sh` runs only Unix-based systems at the moment, `bakery's` use of [`sarge`](https://sarge.readthedocs.io/en/latest/), written by [`Vinay Sajip / vsajip`](https://github.com/vsajip), allows it to run on DOS-based systems, such as `Microsoft Windows`, as well. Here are a few more differences:
* Subcommands cannot be passed in as arguments, only as attributes or as `kwarg settings`, such as the following:
    ```python
    from baker.y import git

    # git status
    git.status()
    ```

    ```python !
    from baker.y import zpool

    # zpool import -f pool_name
    zpool(pool_name, f = True, _subcommand = "import")
    ```

* Program options can be directly set without baking them in first (heresy, I know):
    ```python !
    from baker.i import git

    # git -C working_directory status
    git(C = working_directory).status()
    ```
    `Note:` Because `git` is in a list called `bakeriy_menu`, it can be imported with the ability to set program options when imported using `baker.y`; if not in the `menu`, or if not imported using `baker.i`, programs will not have this ability.

* Arguments are appended to the end of the command; however, arguments can be set at the beginning by using the kwarg setting `_starter_args`, which can be a string or an iterable:
    ```python
    from baker.y import ls, find

    # ls -l -a ~
    ls("~", l = True, a = True)

    # find . -name hello
    find(
        "hello",
        name = True,
        _kwarg_one_dash = True,
        _starter_args = "."
    )
    ```

* While I'm not sure how different the following behavious is, you can iterate over the `bakeriy` object itself to get its output:
    ```python
    from baker.y import ls

    # And no, I didn't miss the brackets;
    # that's what I was confused about initially.

    # ls
    for item in ls:
        print(item)
    ```

* You can use specific shells to run commands as well:
    ```python
    from baker.y import ls

    # bash -c 'ls'
    ls(_shell = "bash")
    ```

* Want to get the the command you're about to run?
    ```python
    from baker.y import ls

    # This time literally

    # bash -c 'ls'
    ls(_shell = "bash", _str = True)
    ```

* Want to *see* the the command you're about to run?
    ```python
    from baker.y import ls

    # This time literally

    # bash -c 'ls'
    ls(_shell = "bash", _print = True)
    ```

* Here's how to use sudo:
    ```python !
    from baker.y import ls

    # sudo -i -u root ls /
    ls("/", _sudo = dict(i = "root"))

    # sudo -s -u root ls /
    ls("/", _sudo = dict(s = "root"))
    ```

* If you want visible prompts, use the kwarg settings `_capture = "run"` or `_run = True`; otherwise, prompts will be captured in the output, while the process still halts for input (help me fix this, please?)
    ```python !
    from baker.y import zfs

    # Will show input prompt

    # zfs load-key pool
    zfs.load_key(pool, _capture = "run")



    # Will NOT show input prompt

    # zfs load-key pool
    zfs.load_key(pool)
    ```
    `Note:` This does not happen with the use of `sudo`, or the `_sudo` kwarg setting; the password prompt will still be shown, and input will still be passed to `sudo`.

* One can "freeze" `bakery` objects, allowing other `bakery` objects to act on them; a frozen `bakery` object has its program replaced by the command, after which `self` is returned:
    ```python
    from baker.y import ls

    # Freeze using a non-truthy value, not including strings or integers

    # ls
    ls([])

    # Some Alternatives
    ls(None)
    ls(False)
    ls(bool(0))
    ls(bool(""))

    # Freeze using the keyword (but it's longer; why would you want to do that? :P)
    ls(_frozen = True)

    # Freeze using... Nothing! :D
    ls
    ```

* Piping and Redirection is implemented through the use of frozen `bakery` objects and strings, as well as through the `_pipe` and `_redirect` kwarg settings:
    ```python
    from os import devnull
    from baker.y import ls, tail

    # Piping using frozen objects

    # ls | tail
    tails = ls | tail
    tails = ls([]) | tail([])
    tails = "ls" | tail([])
    tails = ls([]) | "tail"
    tails()


    # Piping to tee

    # ls | tee /dev/null
    teels = ls ^ devnull
    teels()

    # ls | tee -a /dev/null
    teels = ls + devnull
    teels()

    # Redirection using frozen objects

    # ls > /dev/null
    nulls = ls >> devnull
    nulls()

    # ls > /dev/null
    nulls = ls([]) >> devnull
    nulls()

    # ls 2> /dev/null
    nulls = ls >> (2, devnull)
    nulls()

    # ls >1 /dev/null
    nulls = ls >> (devnull, 1)

    # ls &> /dev/null
    nulls = ls >> ("&", devnull)
    nulls()

    # ls >&1 /dev/null
    nulls = ls >> (devnull, "&1")
    nulls()

    # ls 2>&1 /dev/null
    nulls = ls >> (2, devnull, "&1")

    # ls < /dev/null
    nulls = ls << devnull

    # ls >> /dev/null
    nulls = ls @ devnull
    ```

* `bakery` objects may be used as decorators as well, using the `_d` or `_decorator` kwarg settings:
    ```python !
    from baker.y import ls, zfs

    # ls /
    @ls(_d = True, _run = True)
    def root():
        return "/"
    root()

    # zfs list chimchar
    @zfs.list(_d = True, _run = True)
    def root(pool):
        return pool
    root("chimchar")
    ```

* Context manager functionality exists as well:
    ```python
    import baker.y

    # ls
    with baker.y.ls as _list:
        _list(_run = True)
    ```

***

## Notes

* 

***

## Links

* 

***

## TODO

* Comment
* Documentation
* Implement
    * Buffers

***

## [Saku](https://github.com/kt3k/saku), by [Yoshiya Hinosawa](https://github.com/kt3k)

`Saku` can use this README as well, both to install the module and to upgrade it, as well as for anything else added later on. To do so, run `saku [task]`, such as `saku install`.

<!-- saku start -->

### install

    /usr/bin/env python3 -m pip install .

### upgrade

    /usr/bin/env python3 -m pip install --upgrade .

<!-- saku end -->

***

## Copyright
