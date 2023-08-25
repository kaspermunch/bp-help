


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
      # packages=setuptools.find_packages(),
      # include_package_data=True,
      # packages = ['bp_help'],
      package_dir={'bp_help': 'bp_help'},
      package_data={'bp_help': ['*.css']},
      # packages=find_packages(),
      # package_data={"": ["*.css"]},
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
