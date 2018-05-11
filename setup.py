from setuptools import setup
from setuptools import find_packages


setup(
    name='prophet',
    version='0.1.2',
    install_requires=[
        "pytz>=2014.9",
        "pandas>=0.15.1",
        "pandas-datareader>=0.4.0",
        "seaborn>=0.8",
        "six>=1.8.0"
    ],
    packages=find_packages(),
    author='Michael Su',
    author_email='mdasu1@gmail.com',
    description='Microframework for analyzing financial markets.',
    license="BSD",
    keywords="backtest framework markets financial finance",
    url='http://prophet.michaelsu.io/',
    long_description=open("README.md").read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
