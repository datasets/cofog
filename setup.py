from setuptools import setup, find_packages

setup(
    name='cofog',
    version='0.1',
    license='PDDL',
    description = 'Classification of the Functions of Government',
    package_dir={'cofog': ''},
    packages=find_packages(),
    include_package_data=True,
    # do not zip up the package into an 'Egg'
    zip_safe=False,
)

