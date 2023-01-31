from setuptools import setup

setup(
    name='gcli',
    version='1.0',
    py_modules=['cli', 'gui'],
    install_requires=[
        'Click',
        'requests',
        'sseclient-py',
    ],
    entry_points='''
        [console_scripts]
        gcli=cli:main
    '''
)