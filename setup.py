from setuptools import setup

setup(name='autograder',
        version='0.1',
        description='Autograder for programming projects',
        url='http://github.com/rhomeister/autograder',
        author='Ruben Stranders',
        author_email='r.stranders@gmail.com',
        license='MIT',
        packages=['autograder',
            'autograder.checks',
            'autograder.analysis'],
        install_requires=[
            'gitpython',
            'gitinspector',
            'colorama'
            ],
        entry_points = {
            'console_scripts': [
                'autograder=autograder.cli:main'
                ],
            },
        zip_safe=False
        )

