from setuptools import find_packages, setup

# https://packaging.python.org/guides/distributing-packages-using-setuptools/?highlight=setup.py#setup-py
# Distribute py wheels
# python3 setup.py bdist_wheel sdist
# twine check dist/*
# cd dist
# twine upload *


with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt", "r") as f:
    REQUIREMENTS = f.readlines()


VERSION = "3.0.0"

setup(
    name="licenseware",
    version=VERSION,
    description="Licenseware SDK which contains common functionality used in all apps",
    url="https://licenseware.io/",
    author="Licenseware",
    author_email="contact@licenseware.io",
    license="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=REQUIREMENTS,
    packages=find_packages(where=".", exclude=["tests"]),
    include_package_data=True,
    package_data={"": ["*"]},
    entry_points={
        "console_scripts": [
            "licenseware=licenseware.cli:cli_entrypoint",
        ],
    },
)
