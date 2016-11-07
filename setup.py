from setuptools import setup


def readme():
    with open('README.rst') as fh:
        return fh.read()


setup(
    name='uniques',
    version='0.1',
    description='Filter unique files based on their sha256 hash.',
    long_description=readme(),
    classifiers=[
      'Development Status :: 3 - Alpha',
      'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
      'Programming Language :: Python :: 2.7',
      'Topic :: Utilities',
    ],
    keywords='afl testcases corpus uniques',
    url='http://github.com/yformaggio/uniques',
    author='Yannick Formaggio',
    author_email='yannick@thelumberjhack.org',
    license='GPLv3+',
    packages=['uniques'],
    entry_points={
        'console_scripts': ['uniques=uniques.command_line:main'],
    },
    include_package_data=True,
    zip_safe=False
)