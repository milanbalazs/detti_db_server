import os
import setuptools  # noqa
from distutils.core import setup

try:
    # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:
    # for pip <= 9.0.3
    from pip.req import parse_requirements

# Get the path of the directory of the current file.
PATH_OF_FILE_DIR: str = os.path.realpath(os.path.dirname(__file__))

# Append the path of the tools folder to find modules.
REQ_FILE_PATH = os.path.join(PATH_OF_FILE_DIR, "requirements.txt")


def load_requirements(fname):
    reqs = parse_requirements(fname, session=False)
    try:
        requirements = [str(ir.req) for ir in reqs]
    except AttributeError:
        requirements = [str(ir.requirement) for ir in reqs]
    return requirements


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="detti_db_server",
    version="0.1.0",
    description="Lightweight Json based key-value DB and/or server.",
    long_description_content_type="text/markdown",
    long_description=long_description,
    author="Milan Balazs",
    author_email="milanbalazs01@gmail.com",
    license="three-clause BSD",
    python_requires=">=3.6",
    url="https://github.com/milanbalazs/detti_db_server",
    install_requires=load_requirements(REQ_FILE_PATH),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Developers",
        "Topic :: Database",
        "Operating System :: POSIX",
    ],
    scripts=["tools/color_logger.py"],
    package_data={"": ["tools/*.py", "detti_conf.ini"]},
    packages=["."],
)
