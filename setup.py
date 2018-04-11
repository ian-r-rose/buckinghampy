metadata = dict(
    name= 'buckinghampy',
    version = 1.0,
    description='Educational package for dimensional analysis',
    url='https://github.com/ian-r-rose/buckinghampy',
    author='Ian Rose',
    author_email='ian.r.rose@gmail.com',
    license='GPL',
    long_description='',
    platforms       = "Linux, Mac OS X, Windows",
    packages = ['buckinghampy'],
    python_requires = '>=3.6',
    classifiers     = [
     'Intended Audience :: Developers',
     'Intended Audience :: Education',
     'Intended Audience :: Science/Research',
     'Programming Language :: Python',
     'Programming Language :: Python :: 3',
    ],
    install_requires=[
     'sympy'
    ],
)

from setuptools import setup

setup ( **metadata )
