from setuptools import setup, find_packages

setup(
    name="asset_management",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'mysql-connector-python==8.0.33',
        'bcrypt==4.0.1',
        'pytest==7.4.0',
        'python-dotenv==1.0.0',
        'configparser==5.3.0',
    ],
)