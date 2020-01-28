import os
import setuptools

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-ses-sns-tracker",
    version="1.0.1",
    author="anfema GmbH",
    author_email="contact@anfe.ma",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    url="https://github.com/anfema/django-ses-sns-tracker",
    packages=setuptools.find_packages(),
    classifiers=[
        "Framework :: Django :: 1.11",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 2.2",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'django_ses',
        'requests',
        'cryptography',
        'future;python_version<"3"',
        'typing;python_version<"3.5"',
    ],
    test_suite='runtests.run_tests',
    zip_safe=False,
)
