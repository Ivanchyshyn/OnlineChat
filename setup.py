from setuptools import setup, find_packages
from os import path

BASE_URL = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(BASE_URL, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='aiohttp-socketio-chat',
    version='0.0.1',

    description='Online chat with aiohttp and socket.io as base',
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/Ivanchyshyn/OnlineChat',

    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],

    keywords='aiohttp socketio chat',

    package_dir={'': 'src'},
    packages=find_packages(where='src'),

    python_requires='>=3.7',
    install_requires=[
        'aiohttp>=3', 'aiopg>=1', 'aioredis>=1', 'gunicorn>=20',
        'python-socketio>=4', 'psycopg2-binary>=2', 'SQLAlchemy>=1',
    ],

    entry_points={
        'console_scripts': [
            'runchat=main',
        ],
    },
)
