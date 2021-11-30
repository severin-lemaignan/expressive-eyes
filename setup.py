import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="expressive-eyes",
    version="0.0.2",
    author="Séverin Lemaignan,Catherine Chambers, Batuhan Kaya",
    author_email="severin.lemaignan@pal-robotics.com",
    description="Procedural expressive eyes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=["expressive_eyes"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
