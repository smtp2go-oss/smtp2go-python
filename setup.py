from setuptools import setup

from smtp2go.core import __version__

setup(name='smtp2go',
      version=__version__,
      description='Library for interfacing with the smtp2go API.',
      url='https://github.com/smtp2go-oss/smtp2go-python',
      author='smtp2go',
      author_email='devs@smtp2go.com',
      license='MIT',
      packages=['smtp2go'],
      install_requires=[
          'requests'
      ],
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Topic :: Communications :: Email",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      zip_safe=False)
