


#from distutils.core import setup
from setuptools import setup, find_packages

setup(name='bp_help',
      test_suite='tests',
      version='0.2',
      description='',
      long_description='',
      author='Kasper Munch',
      author_email='kasmunch@birc.au.dk',
      url='',
      # packages = ['bp_help'],
      packages=find_packages(),
      # package_dir = {'bp_help': 'bp_help'},
      entry_points = {
            'console_scripts': [
                  'print-steps=bp_help.print_steps:run_student_file',
                  'myiagi=bp_help.text_gui:run'
                  ],
        },
        install_requires=[
          'pygments',
          'textual',
          'rich',
          'art',
        ]
      )
