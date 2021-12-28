import setuptools

try:
    with open("README.md", "r") as readme:
        long_description = readme.read()
except:
    long_description = ""

setuptools.setup(
    name="aquanta",
    version="0.1",
    author="Jeremy Compostella",
    description="Unofficial library to interact with Aquanta water heater smart controller.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jeremy-compostella/aquanta",
    packages=setuptools.find_packages(),
    classifiers=["Programming Language :: Python :: 3",
                 "License :: OSI Approved :: BSD License",
                 "Operating System :: OS Independent",
                 "Topic :: Home Automation"],
    python_requires='>=3.4',
    install_requires=['requests'])
