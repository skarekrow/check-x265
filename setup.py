import sys
from setuptools import setup

if sys.version_info < (3,):
    exit("Only Python 3 is supported.")

setup(name='check-x265',
      version='1.0',
      description='Creates a report if the directory specified has any files not encoded in HEVC.',
      author='Brandon Schneider',
      author_email='brandonschneider89@gmail.com',
      url='https://github.com/skarekrow/check-x265',
      packages=['check_x265'],
      install_requires=[
          'pymediainfo'
      ],
      entry_points={
          'console_scripts': [
              'check-x265 = check_x265:main'
          ]
      })
