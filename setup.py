from setuptools import setup, find_packages

setup(
    name='djog',
    version='2.0',
    packages=find_packages(),
    install_requires=['cartridge',
                      'bleach',
                      ],
    include_package_data=True,
    url='https://github.com/val-sytch/shop_django2.0',
    author='SoftGroup Python Team ',
    description='Dogs shop on Mezzanine/Cartridge'
)
