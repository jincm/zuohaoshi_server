#install pip and virtualenv
sudo apt-get install -y python-pip
mkdir -p /home/jincm/zuohaoshi
sudo mkdir -p /var/log/zuohaoshi
sudo chmod 777 /var/log/zuohaoshi/

cd /home/jincm/zuohaoshi
sudo apt-get install -y build-essential python
sudo apt-get install -y python-dev
sudo pip install virtualenv
virtualenv venv
source venv/bin/activate

#export first from local,not need on remote when build product environment
pip freeze > requirements.txt

#install from requirments
pip install -r requirements.txt

sudo pip install requests

#163 apt source for ubuntu14.04
#cat /etc/apt/sources.list
deb http://mirrors.163.com/ubuntu/ trusty main restricted universe multiverse
deb http://mirrors.163.com/ubuntu/ trusty-security main restricted universe multiverse
deb http://mirrors.163.com/ubuntu/ trusty-updates main restricted universe multiverse
deb http://mirrors.163.com/ubuntu/ trusty-proposed main restricted universe multiverse
deb http://mirrors.163.com/ubuntu/ trusty-backports main restricted universe multiverse
deb-src http://mirrors.163.com/ubuntu/ trusty main restricted universe multiverse
deb-src http://mirrors.163.com/ubuntu/ trusty-security main restricted universe multiverse
deb-src http://mirrors.163.com/ubuntu/ trusty-updates main restricted universe multiverse
deb-src http://mirrors.163.com/ubuntu/ trusty-proposed main restricted universe multiverse
deb-src http://mirrors.163.com/ubuntu/ trusty-backports main restricted universe multiverse

sudo apt-get install -y redis-server
sudo apt-get install -y nginx
sudo apt-get install -y supervisor
sudo apt-get install -y git

#mongodb
$ vi /etc/hosts
54.192.157.46 repo.mongodb.org

sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
echo "deb http://repo.mongodb.org/apt/ubuntu "$(lsb_release -sc)"/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org

#not need download and install OSS.zip,it was already put into project
sudo apt-get install unzip
OSS_Python_API_20150811.zip

###git clone
git clone https://github.com/jincm/zuohaoshi_server.git server

###deploy
sudo cp nginx_default /etc/nginx/sites-enabled/default
sudo cp supervisor.conf /etc/supervisor/conf.d/supervisor.conf
sudo service nginx restart

###Important!!!!!!!!!!!!!!!!!!!!
###patched to flask/json.py for jsonify(ObjectId)
vi /usr/local/lib/python2.7/dist-packages/flask/json.py
# added by jincm for bug
++from bson import ObjectId
        # added by jincm for jsonify ObjectId
        ++if isinstance(o, ObjectId):
           ++return str(o)
        if isinstance(o, datetime):
            return http_date(o)

###deploy chat server
pushd /usr/local/src
tar xzf node-v4.2.3-linux-x64.tar.gz
ln -fs `pwd`/node-v4.2.3-linux-x64/bin/node /usr/sbin/node
ln -fs `pwd`/node-v4.2.3-linux-x64/bin/npm /usr/sbin/npm
npm -v && node -v
pushd /home/jincm/zuohaoshi/server/chat
npm install --save express
npm install --save socket.io
#test code
git clone https://github.com/plhwin/nodejs-socketio-chat.git

### Run
test can use
$ sudo python manage.py runserver
for production
$sudo /usr/local/bin/uwsgi /home/jincm/zuohaoshi/server/uwsgi_config.ini


### Testing
#install ab for test
sudo apt-get install -y apache2-utils
sudo apt-get install -y curl
./test/mycurl.sh

With coverage:
```sh
$ python manage.py cov

Change Log
----------
**v0.4** - user/activity/face++/easemob
**v0.3** - register/login/logout/redis/mongodb
**v0.2** - Return token.
**v0.1** - Initial release.
----------
