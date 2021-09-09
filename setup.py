from setuptools import setup, find_packages

VERSION = '0.1.0'
DESCRIPTION = 'Generate graphs from the stochastic block model.'
LONG_DESCRIPTION =\
    "Tools for generating graphs from the stochastic block model."

# Setting up
setup(
    name="sbm",
    version=VERSION,
    author="Peter Macgregor",
    author_email="<macgregor.pr@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
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