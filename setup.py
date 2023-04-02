from setuptools import setup, find_packages

setup(
    name="pingmonitor"
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        # Add your package's dependencies here
    ],
    author="Cary Carter",
    author_email="ccarterdev@gmail.com",
    description="using ping and google dns to determine network latency/packet loss/quality in geleral",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/cc-d/pingmonitor",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
)
