from setuptools import setup

setup(name='smtp2go',
      version='0.0.1-alpha',
      description='Library for interacting with the SMTP2Go API.',
      url='https://github.com/smtp2go/smtp2go.api-python',
      author='SMTP2Go',
      author_email='smtp2go@david-bush.co.uk',
      license='MIT',
      packages=['smtp2go'],
      install_requires=[
          'requests'
      ],
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries"
      ],
      zip_safe=False)
