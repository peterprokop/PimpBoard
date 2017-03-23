# Installation

Install virtualenv
`pip3 install virtualenv`

Create new environment:
`virtualenv MYVIRTUALENV`

Activate it
`source MYVIRTUALENV/bin/activate`

Install PostgreSQL, create user `pimp` with password `changeme`

Run 
```
python pimp_board/manage.py db init
python pimp_board/manage.py db migrate
python pimp_board/manage.py db upgrade
```

to put database in shape.

After that:
```
pip3 install --editable .
./run_debug.sh
```
