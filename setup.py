from setuptools import setup

setup(
    name="tidyhome",
    version="0.1.0",
    packages=["tidyhome"],
    install_requires=[],
    entry_points={
        "console_scripts": [
            "tidyhome = tidyhome.cli:main"
        ]
    }
)