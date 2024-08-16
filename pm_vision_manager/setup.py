from setuptools import setup
import os

package_name = 'pm_vision_manager'
submodules = 'pm_vision_manager/va_py_modules'
app_modules = 'pm_vision_manager/va_py_modules/vision_app_modules'
vision_functions = 'pm_vision_manager/va_py_modules/feature_detect_functions'


data_files=   [    
    ('share/ament_index/resource_index/packages',
    ['resource/' + package_name]),
    ('share/' + package_name, ['package.xml']),
    ('share/' + package_name, ['config/vision_assistant_path_config.yaml']),  
    ('share/' + package_name, ['config/vision_assistant_config.yaml']),
    ('share/' + package_name + '/launch', ['launch/pm_vision.launch.py']),
    ]


def package_files(data_files, directory_list):

    paths_dict = {}

    for directory in directory_list:

        for (path, directories, filenames) in os.walk(directory):

            for filename in filenames:

                file_path = os.path.join(path, filename)
                install_path = os.path.join('share', package_name, path)

                if install_path in paths_dict.keys():
                    paths_dict[install_path].append(file_path)

                else:
                    paths_dict[install_path] = [file_path]

    for key in paths_dict.keys():
        data_files.append((key, paths_dict[key]))

    return data_files


setup(
    #author='Niklas Terei',
    #author_email='terei@match.uni-hannover.de',
    #maintainer='Niklas Terei',
    #maintainer_email='terei@match.uni-hannover.de',
    name=package_name,
    version='0.1.0',
    packages=[package_name, submodules, app_modules,vision_functions],
    data_files=package_files(data_files,['vision_functions/']),
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
