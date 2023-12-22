from setuptools import setup,find_packages

setup(
    name='ME2_Beleg',
    version='0.0.1',
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "scipy"
    ],
    packages=find_packages(
    include=["me2","me2.*"])
)