sudo pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

#requirements may include some package like this
sudo pip install pymongo
sudo pip install passlib
sudo pip install itsdangerous
sudo pip install flask-script

#install ab for test performance
sudo apt-get install apache2-utils

sudo apt-get install mongodb-org


### Run
```sh
$ python manage.py runserver
```

### Testing
Without coverage:
```sh
$ python manage.py test
```

With coverage:
```sh
$ python manage.py cov

Change Log
----------
**v0.2** - Return token.
**v0.1** - Initial release.
----------
