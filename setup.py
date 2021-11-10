from setuptools import setup, find_packages

VERSION = '0.2.1'
DESCRIPTION = 'Deprecated in favour of SGTL.'
LONG_DESCRIPTION =\
    "This project has been absorbed by the SGTL - Spectral Graph Theory Library." \
    "See [the documentation](https://sgtl.readthedocs.io/en/latest/)"

# Setting up
setup(
    name="sbm",
    version=VERSION,
    author="Peter Macgregor",
    author_email="<macgregor.pr@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["numpy", "scipy"],

    keywords=['python', 'graph', 'sbm', 'stochastic block model', 'algorithms'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        'Operating System :: POSIX :: Linux'
    ]
)
