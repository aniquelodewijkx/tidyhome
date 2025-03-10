from setuptools import setup

setup(
    name="tidyhome",
    version="0.1.0",
    packages=["tidyhome"],
    install_requires=[
        "inquirer"
    ],
    entry_points={
        "console_scripts": [
            "tidyhome = tidyhome.tidier:main"
        ]
    }
)