#!/usr/bin/env mdsh
# bakery

***

## Welcome to the `bakery`! May I wrap your program?

&nbsp;&nbsp;&nbsp;&nbsp; `bakery` is a python module heavily inspired by [`sh`](https://amoffat.github.io/sh/), written by [`Andrew Moffat / amoffat`](https://github.com/amoffat); I loved the concept of `baking` a command so much that I created an entire module based on it.

&nbsp;&nbsp;&nbsp;&nbsp; While amoffat's `sh` runs only Unix-based systems at the moment, `bakery's` use of [`sarge`](https://sarge.readthedocs.io/en/latest/), written by [`Vinay Sajip / vsajip`](https://github.com/vsajip), allows it to run on DOS-based systems, such as `Microsoft Windows`, as well. Here are a few more differences:
* Subcommands cannot be passed in as arguments, only as attributes or as `kwarg settings`, such as the following:
    ```python
    from baker.y import git, zpool

    # git status
    git.status()

    # zpool import -f pool_name
    zpool(pool_name, f = True, _subcommand = "import")
    ```

* Program options can be directly set without baking them in first (heresy, I know):
    ```python
    from baker.i import git

    # git -C working_directory status
    git(C = working_directory).status()
    ```
    `Note:` Because `git` is in a list called `bakeriy_menu`, it can be imported with the ability to set program options when imported using `baker.y`; if not in the `menu`, or imported using `baker.i`, programs will not have this ability.

* Arguments are appended to the end of the command; however, arguments can be set at the beginning by using the kwarg setting `_starter_args`, which can be a string or an iterable:
    ```python
    from baker.y import ls, find

    # ls -l -a ~
    ls("~", l = True, a = True)

    # find . -name bakery
    find(
        "bakery",
        name = True,
        _kwarg_one_dash = True,
        _starter_args = "."
    )
    ```

* While I'm not sure how different the following behavious is, you can iterate over the `bakery` object itself to get its output:
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
    * Piping
    * Redirection
    * Buffers

***

## Saku

<!-- saku start -->

### install

    /usr/bin/env python3 -m pip install .

### upgrade

    /usr/bin/env python3 -m pip install --upgrade .

<!-- saku end -->

***

## Copyright
