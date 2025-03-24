# setup.py
from setuptools import setup, find_packages

setup(
    name="zapnet",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    entry_points={
        'console_scripts': [
            'zapnet=zapnet.cli:cli',
        ],
    },
)