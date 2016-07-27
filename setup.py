from setuptools import setup

setup(name='tvsongs',
      version='0.2',
      description='Find and listen to songs featured in TV shows.',
      keywords='find search listen tv show series songs music featured',
      url='https://github.com/zvovov/tvsongs',
      author='Chirag Khatri',
      author_email='zvovov@gmail.com',
      license='MIT',
      packages=['tvsongs'],
      scripts=['bin/tvsongs'],
      install_requires=[
          'beautifulsoup4',
          'requests',
          'python-slugify',
      ],
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Multimedia',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Multimedia :: Sound/Audio :: Analysis',
        'Topic :: Text Processing :: General',
      ],
      include_package_data=True,
      zip_safe=False)