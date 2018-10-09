import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BingTTS",
    version="0.0.1",
    author="Marvin Benitez",
    author_email="mjbb20122@hotmail.com",
    description="A wrapper to link python to the Bing API REST",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JoseDev2018/BingTTS",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
)
