from setuptools import setup

cmdclass={}

try:
    from sphinx.setup_command import BuildDoc
    cmdclass['build_sphinx'] = BuildDoc
except ImportError:
    print('WARNING: sphinx not available, not building docs')

requires=[ 
    'requests', 
    'tabulate', 
    'six', 
    'enum34; python_version == "2.7"', 
    'configparser; python_version == "2.7"', 
    'polling', 
    'fire' 
  ]

setup(
  name='hpecp',
  description="HPE Container Platform client",
  author='Chris Snow',
  author_email='chsnow123@gmail.com',
  url='https://github.com/hpe-container-platform-community/hpecp-python-library',
  packages = ['hpecp'],
  scripts=['bin/hpecp'],
  keywords = '',
  install_require=requires,
  test_suite='nose.collector',
  tests_require=['nose', 'mock'],
  setup_requires=requires,
  cmdclass=cmdclass,
  command_options={
        'build_sphinx': {
            'project': ('setup.py', 'HPE Container Platform client'),
            'version': ('setup.py', 'pre-alpha'),
            'release': ('setup.py', 'n/a'),
            'source_dir': ('setup.py', 'docs/source'),
            'build_dir': ('setup.py', 'docs/build'),
            }
        },
  classifiers=[
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
  ],
)
