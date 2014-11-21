from setuptools import setup

setup(
    name='prophet',
    version='0.1.0',
    description='Microframework for analyzing financial markets.',
    author='Michael Su',
    author_email='mdasu1@gmail.com',
    url='http://prophet.michaelsu.io/',
    install_requires=[
        "pytz>=2014.9",
        "pandas>=0.15.1",
    ],
    packages=['prophet'],
)
