from distutils.core import setup
setup(
  name = 'meroshare', 
  packages = ['meroshare'],
  version = '0.1', 
  license='MIT', 
  description = 'A python package to interact with meroshare', 
  author = 'Saurav Pathak', 
  author_email = 'saurab.pathak.0@gmail.com', 
  url = 'https://gitlab.com/saurab.pathak.0/meroshare.git',
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['nepal', 'meroshareapi', 'stockmarketAPI'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'validators',
          'beautifulsoup4',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)