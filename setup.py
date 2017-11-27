from setuptools import setup


setup(
    name='idlewild',
    version='0.4.0',
    packages=['idlewild'],
    author='Gary Anderson',
    author_email='gary.anders@gmail.com',
    url='http://github.com/gando999/idlewild/',
    description='GraphQL IDL Parser',
    install_requires=[
        'ply==3.10',
        'pyparsing==2.0.3',
        'wheel==0.24.0',
        'graphql-core>=2.0',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Database :: Front-Ends',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
