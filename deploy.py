import os
from fabric import Connection


if __name__ == '__main__':
    c = Connection(
        host=os.getenv('FARIASWEB_HOST'),
        connect_kwargs={
            'password': os.getenv('FARIASWEB_PASSWORD')
        }
    )
    c.run('cd fariasweb && git pull')
    c.run('supervisorctl stop fariasweb')
    c.run(
        'export LC_ALL=C.UTF-8 '
        '&& export LANG=C.UTF-8 '
        '&& export FLASK_APP=fariasweb.py '
        '&& cd fariasweb '
        '&& source venv/bin/activate '
        '&& flask db upgrade'
    )
    c.run('supervisorctl start fariasweb')
