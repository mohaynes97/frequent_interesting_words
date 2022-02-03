from setuptools import find_packages, setup

setup(
    name="frequent_interesting_words",
    version="0.0.0",
    py_modules=["frequent_interesting_words"],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "frequent-interesting-words = frequent_interesting_words.cli:frequent_interesting_words",
        ],
    },
)
