from setuptools import setup, find_packages

setup(
    name='tidyhome',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'inquirer',
    ],
    entry_points={
        'console_scripts': [
            'tidyhome=tidyhome.tidier:main',
        ],
    },
    package_data={
        '': ['tasks.json'],
    },
    author='Anique Lodewijkx',
    author_email='anique.lodewijkx@gmail.com',
    description='A random task assignment tool for tidying up your home',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/tidyhome',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)