import setuptools

with open('README.md', 'r') as readme:
    long_description = readme.read()

setuptools.setup(
    name='aquanta',
    version='0.2',
    author='Jeremy Compostella',
    author_email='jeremy.compostella@gmail.com',
    description='Unofficial library to interact with Aquanta water heater smart controller.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jeremy-compostella/aquanta',
    classifiers=['Programming Language :: Python :: 3',
                 'License :: OSI Approved :: BSD License',
                 'Operating System :: OS Independent',
                 'Topic :: Home Automation'],
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    python_requires='>=3.6',
    install_requires=['requests'])
