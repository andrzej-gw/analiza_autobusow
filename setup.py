import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    setuptools.setup(
    name="analizaautobusow-pkg-ANDRZEJ-GWIAZDA",
    version="0.0.1",
    author="Andrzej Gwiazda",
    author_email="jedrekgwiazda@gmail.com",
    description="Pakiet do analizy autobusow.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.mimuw.edu.pl/ag448511/projekt_python.git",
    packages=setuptools.find_packages(),
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    )
