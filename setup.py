import os
import setuptools


with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

setuptools.setup(
    author="Zagaran, Inc.",
    author_email="info@zagaran.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    description="Command line tool to manage AWS CLI credentials with MFA (multi-factor authentication)",
    entry_points={
        "console_scripts": ["iam-mfa=iam_mfa.iam_mfa:main"],
    },
    install_requires=[],
    keywords="aws cli iam mfa",
    license="MIT",
    long_description=README,
    long_description_content_type="text/markdown",
    name="iam-mfa",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    url="https://github.com/zagaran/iam-mfa",
    version="0.0.1",
)
