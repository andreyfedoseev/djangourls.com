from setuptools import setup, find_packages

setup(
    name="djangourls",
    version="dev",
    package_dir={"": "apps", "project": "./project"},
    packages=find_packages("apps") + ["project"],
)
