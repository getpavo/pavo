#!/usr/bin/env python3
import setuptools

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(name='pavo',
                 version='0.1.0',
                 description='Static Site Generation using Python made easy.',
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 author='Job Veldhuis',
                 author_email='job@baukefrederik.me',
                 python_requires='>=3.6',
                 url='https://github.com/getpavo/pavo',
                 classifiers=[
                     'Programming Language :: Python :: 3',
                     'Development Status :: 2 - Pre-Alpha',
                     'License :: OSI Approved :: MIT License',
                     'Operating System :: OS Independent'
                 ],
                 install_requires=[
                     'markdown2>=2.3.9',
                     'httpwatcher>=0.5.2',
                     'Jinja2>=2.11.3',
                     'requests>=2.25.1',
                     'tornado>=4.5.3',
                     'libsass>=0.20.1',
                     'python_frontmatter>=1.0.0',
                     'PyYAML>=5.4.1'
                 ],
                 entry_points={
                     'console_scripts': [
                         'pavo=pavo.cli._cli:_main'
                     ],
                     'pavo_commands': [
                         'help=pavo.cli._cli:_help',
                         'build=pavo.core._build:main',
                         'create=pavo.core._create:main',
                         'deploy=pavo.core._deploy:main',
                         'dev=pavo.core._dev:main'
                     ]
                 },
                 packages=setuptools.find_packages()
                 )
