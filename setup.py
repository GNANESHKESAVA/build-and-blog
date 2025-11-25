from setuptools import setup, find_packages

setup(
    name="codeinspector",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click",
        "gitpython",
        "pygithub",
        "google-generativeai",
    ],
    entry_points={
        "console_scripts": [
            "codeinspector=codeinspector.cli:codeinspector",
        ],
    },
)
