from setuptools import setup, find_packages

setup(
    name='barsystem',
    version='1.0.1',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'barsystem-installer = barsystem.install:main'
        ]
    },

    install_requires=[
        'django>=1.10,<=1.10.99',
        'django-translatable',
        'pytz',
        'python-dateutil',
        'Pillow',
    ],
    extras_require={
        'uwsgi': ['uwsgi'],
        'mqtt': ['paho-mqtt'],
    },

    license='MIT',
    description='',
    long_description='',
    url='https://github.com/TkkrLab/barsystem',
    author='Jasper Seidel',
    author_email='code@jawsper.nl',
)
