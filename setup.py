from setuptools import setup

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setup(
    name='Serial-for-controller',
    version='0.0.1',
    packages=['Serial'],
    url='https://github.com/Adam-Software/Serial-for-controller',
    license='MIT',
    author='vertigra',
    author_email='a@nesterof.com',
    description='Python library for data exchange with adam controller',
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_data={'Serial': ['*.so']},
    include_package_data=True,
    install_requires=['numpy'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Other',
        'Programming Language :: C',
        'Programming Language :: Python :: 3'
    ]
)
