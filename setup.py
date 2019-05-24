from distutils.core import setup


setup(name='bozbo',
      version='0.0.0',
      description='Fast fake API',
      install_requires=[
          'bottle==0.12.16',
          'Faker==1.0.7'
      ],
      packages=['bozbo'],
      entry_points = {
          'console_scripts': [
              'bozbo = bozbo.__main__:main',
          ]
      }
)
