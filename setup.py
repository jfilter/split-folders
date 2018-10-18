from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

classifiers = [
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'License :: OSI Approved :: MIT License',
    'Topic :: Utilities']

setup(name='split_folders',
      version='0.2.0',
      description='🗂 Split folders with files (e.g. images) into training, validation and test (dataset) folders.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/jfilter/split-folders',
      author='Johannes Filter',
      author_email='hi@jfilter.de',
      license='MIT',
      packages=['split_folders'],
      classifiers=classifiers,
      scripts=['bin/split_folders'])
