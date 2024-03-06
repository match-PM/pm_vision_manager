from setuptools import setup

package_name = 'pm_vision_app'
submodules = 'pm_vision_app/py_modules'
setup(
    #author='Niklas Terei',
    #author_email='terei@match.uni-hannover.de',
    #maintainer='Niklas Terei',
    #maintainer_email='terei@match.uni-hannover.de',
    name=package_name,
    version='0.1.0',
    packages=[package_name, submodules],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        #('share/' + package_name, ['pm_vision_app.py']),
        ('share/' + package_name, ['pm_vision_app/vision_assistant_app.py']),

        
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Niklas Terei',
    maintainer_email='terei@match.uni-hannover.de',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
