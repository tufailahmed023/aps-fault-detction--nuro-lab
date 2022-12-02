from setuptools import find_packages,setup
from typing import List

REQUIRMENT_FILE_NAME = 'requirements.txt'
hyphen_e_dot = '-e .'

def get_requirements() -> List[str]:
    with open (REQUIRMENT_FILE_NAME) as requirements_file:
        requirements_list = requirements_file.readlines()
    requirements_list = [rerequirements_name.replace("\n","") for rerequirements_name in requirements_list]

    if hyphen_e_dot in requirements_list:
        requirements_list.remove(hyphen_e_dot)
    return requirements_list



setup(
    name="sensor",
    version="0.0.1",
    author="tufail",
    author_email="tufailahmed023@gmail.com",
    packages = find_packages(),
    install_requires=get_requirements(),
)