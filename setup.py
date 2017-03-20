from setuptools import setup

setup(
    name='pimp_board',
    packages=['pimp_board'],
    include_package_data=True,
    install_requires=[
        'flask',
        'psycopg2',
        'Flask-SQLAlchemy',
        'Flask-Migrate',
        'flask-login==0.2.7'
    ],
)