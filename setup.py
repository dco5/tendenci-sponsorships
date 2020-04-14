from setuptools import setup, find_packages

longdesc = \
    '''
    An addon for Tendenci for accepting Sponsorships for events.
    '''

setup(
    name='tendenci-sponsorships',
    author='Jaime Lossada',
    author_email='jlosada87@hotmail.com',
    version='7.1.1',
    license='GPL3',
    description='Sponsorships addon for Tendenci',
    long_description=longdesc,
    url='https://github.com/dco5/tendenci-sponsorships',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    include_package_data=True,
    packages=find_packages(),
    install_requires=['tendenci>=7.0,<8.0', 'django-widget-tweaks>=1.4'],
)
