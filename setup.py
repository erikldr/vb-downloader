from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="vb-downloader",
    version="0.1.0",
    author="Erik Rocha",
    author_email="e.lucasrocha@gmail.com",
    description="Aplicativo para download automático do programa 'A Voz do Brasil'",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seu-usuario/vb-downloader",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",
        "appdirs>=1.4.4",
    ],
    entry_points={
        "console_scripts": [
            "vb-downloader=vb_downloader.gui:main",
        ],
    },
    include_package_data=True,
)
