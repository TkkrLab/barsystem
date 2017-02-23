from setuptools import setup, find_packages

setup(
    name='barlink',
    version='1.0.0',
    packages=find_packages('src'),
    package_dir={'': 'src'},

    entry_points={
        'console_scripts': [
            'barlink = barlink.websocket:main',
        ]
    },

    install_requires=[
        'pyserial',
    ],

    license='MIT',
    description='Compact WebSocket server for barsystem',
    long_description=open('README.md').read(),
    url='https://github.com/TkkrLab/barsystem',
    author='Jasper Seidel',
    author_email='code@jawsper.nl',
)
