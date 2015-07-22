from distutils.core import setup

setup(
    name='aster-accounting',
    version='0.0.2',
    packages=['aster-accounting', 'aster-accounting.pyrad.pyrad', 'aster-accounting.pyrad.pyrad.tests'],
    url='lanbilling.ru',
    license='GPL',
    author='Andrew Tkachenko',
    author_email='trockiy@gmail.com',
    description='Radius accounting client for Asterisk PBX',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Communications :: Email',
        'Topic :: Office/Business',
        'Topic :: Software Development :: Bug Tracking',
    ]
)
