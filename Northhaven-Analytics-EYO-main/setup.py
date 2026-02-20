from setuptools import setup, find_packages


setup(
    name="northavenanalytics-eyo",
    version="1.0.0",
    packages=find_packages(),
    author="Northhaven Analytics",
    author_email="info.northhavenanalytics@gmail.com",
    install_requires=[
        "pandas",
        "numpy",
        "sentence-transformers",
        "torch",
        "fpdf2",
    ],
)