import os

from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt", "r") as f:
    REQUIREMENTS = f.readlines()


VERSION = os.getenv("PACKAGE_VERSION", "3.0.0")


EXTRAS = {
    "dashboard": [
        "flower==1.2.0",
    ],
    "dotenv": [
        "pydantic[dotenv]",
    ],
    "data": [
        "pandas~=1.2",
    ],
    "mongo": [
        "pymongo==4.2.0",
    ],
    "upload": [
        "python-multipart==0.0.5",
    ],
    "metrics": [
        "prometheus-fastapi-instrumentator~=5.9",
    ],
    "tracing": [
        "opentelemetry-api~=1.13",
        "opentelemetry-sdk~=1.13",
        "opentelemetry-exporter-jaeger~=1.13",
        "opentelemetry-instrumentation~=0.34b0",
    ],
    "jwt": [
        "PyJWT~=2.6",
    ],
    "http": [
        "requests~=2.28",
    ],
    "caching": [
        "redis~=4.3",
    ],
    "kafka": [
        "confluent-kafka~=1.9",
    ],
    "testing": [
        "coverage-badge<1",
        "coverage<7",
        "pytest-mock<3",
        "pytest<7",
        "black==22.8.0",
        "honcho==1.1.0",
        "werkzeug",
    ],
}

EXTRAS["all"] = list(set(sum(EXTRAS.values(), [])))

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
    # include_package_data=True,
    # package_data={"": ["*"]},
    extras_require=EXTRAS,
)
