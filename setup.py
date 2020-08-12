import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

README = open(os.path.join(here, 'README.rst')).read()

setup(
    name='drf-reset-password',
    version='1.2.2',
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    description='Description',
    long_description=README,
    author='linnify',
    zip_safe=False,
    author_email='info@linnify.com',
    url='https://github.com/linnify/drf-reset-password',
    license='MIT',
    install_requires=[
        'Django>=3.0',
        'djangorestframework>=3.11'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Framework :: Django',
        'Framework :: Django :: 3.0',
      ],
)