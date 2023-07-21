


from distutils.core import setup

setup(name='bp_help',
      test_suite='tests',
      version='0.1',
      description='',
      long_description='',
      author='Kasper Munch',
      author_email='kasmunch@birc.au.dk',
      url='',
      # packages = ['bp_help'],
      package_dir = {'bp_help': 'bp_help'},
      entry_points = {
            'console_scripts': [
                  'print-steps=bp_help.print_steps:run_student_file',
                  'steps-of-doom=bp_help.game:order_steps'
                  ],
        }      
      )
