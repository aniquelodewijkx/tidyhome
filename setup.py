from setuptools import setup

setup(
    name="tidyhome",
    version="0.1.0",
    packages=["tidyhome"],
    include_package_data=True,
    package_data={"tidyhome": ["task_completions.csv"]},
    install_requires=[
        "inquirer",
        "pandas"
    ],
    entry_points={
        "console_scripts": [
            "tidyhome = tidyhome.tidier:main"
        ]
    }
)