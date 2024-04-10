from setuptools import find_packages, setup

package_name = 'line_follower'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    package_data={'': ['msg/*.msg']},
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='armmy2530',
    maintainer_email='sutigran2557@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'my_node = line_follower.my_node:main',
            'image_pub = line_follower.image_pub:main',
            'image_sub = line_follower.image_sub:main'
        ],
    },
)
