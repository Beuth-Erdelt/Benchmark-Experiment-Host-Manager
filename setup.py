import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="bexhoma",
    version="0.8.12",
    author="Patrick K. Erdelt",
    author_email="perdelt@beuth-hochschule.de",
    description="This python tools helps managing DBMS benchmarking experiments in a Kubernetes-based HPC cluster environment. It enables users to configure hardware / software setups for easily repeating tests over varying configurations.",
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
    python_requires='>=3.10.2',
    include_package_data=True,
    install_requires=requirements,
    package_dir={'bexhoma': 'bexhoma'},
    entry_points='''
        [console_scripts]
        tpch=bexhoma.scripts.tpch:do_benchmark
        tpcds=bexhoma.scripts.tpcds:do_benchmark
        bexperiments=bexhoma.scripts.experimentsmanager:manage
    ''',
)
