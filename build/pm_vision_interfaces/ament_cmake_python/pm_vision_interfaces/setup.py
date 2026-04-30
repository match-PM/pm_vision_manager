from setuptools import find_packages
from setuptools import setup

setup(
    name='pm_vision_interfaces',
    version='0.0.0',
    packages=find_packages(
        include=('pm_vision_interfaces', 'pm_vision_interfaces.*')),
)
