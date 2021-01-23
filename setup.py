from pathlib import Path

import setuptools

setuptools.setup(
    name="touchbar-lyric",
    version="0.5.3",
    author="Chenghao",
    python_requires=">3.7.0",
    author_email="mouchenghao@gmail.com",
    description="Show time-synced lyric with BTT!",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/ChenghaoMou/touchbar-lyric",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests",
        "osascript",
        "cachier",
        "hanziconv",
        "pinyin",
        "regex",
        "loguru",
        "pycrypto",
        "textdistance",
        "numpy",
        "qqmusic-api",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
    ],
)
