from setuptools import setup

setup(
    name='jira-bulk-loader',
    version='0.3.0',
    packages=['jirabulkloader', 'jirabulkloader.test'],
    author='Alexander Dudko',
    author_email='alex.dudko@gmail.com',
    license='Apache 2.0',
    url='https://github.com/oktopuz/jira-bulk-loader',
    scripts=['bin/jira-bulk-loader.py'],
    description='Create tasks in Jira via RESTful API',
    install_requires=[
        "simplejson >= 3.8.1",
        "requests >= 2.9.1",
        "pytest >= 2.8.5",
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Information Technology',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
        'License :: OSI Approved :: Apache Software License',
    ],
)
