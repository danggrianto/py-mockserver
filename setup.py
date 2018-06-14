import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-mockserver",
    version="0.0.2",
    author="Daniel Anggrianto",
    author_email="d.anggrianto@gmail.com",
    description="Python client for mockserver",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/danggrianto/py-mockserver",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests'
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
