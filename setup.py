# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bakery']

package_data = \
{'': ['*']}

install_requires = \
['oreo @ git+https://github.com/syvlorg/oreo.git@main']

setup_kwargs = {
    'name': 'bakery',
    'version': '2.0.0.0',
    'description': 'An "sh" alternative',
    'long_description': None,
    'author': 'sylvorg',
    'author_email': 'jeet.ray@syvl.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)

