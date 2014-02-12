import codecs
import setuptools
import sys


version = '3.6.1'
shortdesc = 'iCalendar parser/generator'
longdesc = codecs.open('README.rst', encoding='utf-8').read()
longdesc += codecs.open('CHANGES.rst', encoding='utf-8').read()
longdesc += codecs.open('LICENSE.rst', encoding='utf-8').read()


tests_require = []
if sys.version_info[:2] == (2, 6):
    # Python unittest2 only needed for Python 2.6
    tests_require = ['unittest2']


setuptools.setup(
    name='icalendar',
    version=version,
    description=shortdesc,
    long_description=longdesc,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        ],
    keywords='calendar calendaring ical icalendar event todo journal '
             'recurring',
    author='Plone Foundation',
    author_email='plone-developers@lists.sourceforge.net',
    url='https://github.com/collective/icalendar',
    license='BSD',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'python-dateutil',
        'pytz',
    ],
    extras_require={
        'test': tests_require
    }
)
