import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="bexhoma",
    version="0.5.4",
    author="Patrick Erdelt",
    author_email="perdelt@beuth-hochschule.de",
    description="This Python tools helps managing DBMS Benchmarking experiments in a HPC cluster environment. It supports AWS and Kubernetes (K8s).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Beuth-Erdelt/Benchmark-Experiment-Host-Manager",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    license="GNU Affero General Public License v3",
    python_requires='>=3.6',
    include_package_data=True,
    install_requires=requirements,
    package_dir={'bexhoma': 'bexhoma'},
)