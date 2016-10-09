import re
from setuptools import setup


version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open("bal/bal.py").read(),
    re.M
    ).group(1)


with open("README.rst", "rb") as f:
    long_descr = f.read().decode("utf-8")


setup(
    name = "bal",
    packages = ["bal"],
    install_requires = ["dnspython"],
    entry_points = {
        "console_scripts": ['bal = bal.bal:main']
        },
    version = version,
    description = "Find the balance of any Bitcoin address via the dnscoin DNS interface.",
    license = "BSD",
    classifiers = [
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],
    long_description = long_descr,
    author = "dnscoin",
    author_email = "hello@dnscoin.nz",
    url = "http://dnscoin.nz/",
    )
