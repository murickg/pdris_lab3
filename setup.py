from setuptools import setup, find_packages

setup(
    name='flask_app',
    version='0.1',
    description='Edu project Flask&PostgreSQL',
    author='Murad Gamzatov',
    packages=find_packages(),
    install_requires=[
        'Flask',
        'psycopg2-binary'
    ],
    extras_require={
        'dev': [
            'pytest',
            'pytest-flask',
            'pytest-cov'
        ],
    },
    entry_points={
        'console_scripts': [
            'flask_app=app.app:main',
        ],
    },
)