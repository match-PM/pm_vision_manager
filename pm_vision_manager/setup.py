from setuptools import setup

package_name = 'pm_vision_manager'
submodules = 'pm_vision_manager/va_py_modules'
app_modules = 'pm_vision_manager/va_py_modules/vision_app_modules'
setup(
    #author='Niklas Terei',
    #author_email='terei@match.uni-hannover.de',
    #maintainer='Niklas Terei',
    #maintainer_email='terei@match.uni-hannover.de',
    name=package_name,
    version='0.1.0',
    packages=[package_name, submodules, app_modules],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name, ['config/vision_assistant_path_config.yaml']),
        ('share/' + package_name + '/launch', ['launch/pm_vision.launch.py']),
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
            'vision_node = pm_vision_manager.vision_node:main',
            'vision_subscriber = pm_vision_manager.vision_sub:main',
            'vision_webcam_publisher = pm_vision_manager.webcam_image_pub:main',
        ],
    },
)
