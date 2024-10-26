from setuptools import setup, find_packages

setup(
    name="scriptblocks",
    version="0.0.0",
    author="OmgRod",
    description="Package used by ScriptBlocks IDE to make apps with Python",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ScriptBlocks/ScriptBlocks.py",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'scriptblocks=scriptblocks.cli:main',
        ],
    },
)
