####################################################################################
####################################################################################
####################################################################################
#普通用户运行docker
sudo gpasswd -a ${USER} docker
sudo service docker restart
sudo chmod a+rw /var/run/docker.sock

# export/import docker image
docker export dockerid > app_server.tar
cat app_server.tar | sudo docker import - zuohaoshi/app_server
或者
docker import http://example.com/exampleimage.tgz zuohaoshi/app_server

###if use docker,then
docker run --name=app_server -p 8080:8080 -p 222:22 -it zuohaoshi/app_server /bin/bash
docker start app_server
docker attach app_server(注意：attach时不能exit，须ctrl+p+q)
#docker run -d -it -P --name docker_name image_name

# 在服务器上运行mongodb，不和redis一台机器，ubuntu14为base的docker运行mongodb，mongod会挂掉
# mkdir -p /data/db
# service mongodb start
# docker里面
# 开启ssh服务后，就可以用服务器的ip+222去ssh登陆docker
service ssh start
service redis-server start && /usr/local/bin/uwsgi /home/jincm/zuohaoshi/server/uwsgi_config.ini && service nginx start
kill -9 `pidof uwsgi` && sleep 1 && /usr/local/bin/uwsgi /home/jincm/zuohaoshi/server/uwsgi_config.ini
#查看settings.py中连接的redis mongodb的ip是否正确，netstat有没有相应的连接

# docker 挂载目录
   -v /etc/:/opt/etc/:ro #read only


# cp /home/jincm/zuohaoshi/server/nginx_default /etc/nginx/sites-available/default
# cp /home/jincm/zuohaoshi/server/supervisor.conf /etc/supervisor/conf.d/supervisor.conf
# ln -fs ../bower_components bower_components

# docker里自动启动服务
放到/etc/rc.local中不好使；
/etc/init.d/ssh start
/etc/init.d/supervisor start
# supervisor在ubuntu14中有问题，监听的进程挂了后重启启动进程失败，端口被supervisor占用！！！

# vm时间不准确：hwclock -s

# client 和nodejs的包最好是压缩后传输，否则连接文件可能link不对：
http://www.foreverpx.cn/2014/11/29/Linux%E4%B8%ADnpm%E5%87%BA%E7%8E%B0npmlog%E6%89%BE%E4%B8%8D%E5%88%B0%E7%9A%84%E8%A7%A3%E5%86%B3%E6%96%B9%E6%B3%95/

### Run
# test can use when develop
$ sudo python manage.py runserver

# python debug
cp pycharm-debug.egg from pycharm install directory
easy_install pycharm-debug.egg
setup pycharm
import pydevd
pydevd.settrace('192.168.3.1', port=12345, stdoutToServer=True, stderrToServer=True)


####################################################################################
####################下面是具体的构建开发环境过程，有上面的docker就不需要了##########
####################################################################################
#install pip and virtualenv
sudo apt-get update 
sudo apt-get install -y python-pip git
mkdir -p /home/jincm/zuohaoshi && sudo mkdir -p /var/log/zuohaoshi 
# sudo chmod 777 /var/log/zuohaoshi/


# venv is not needed when use docker
# cd /home/jincm/zuohaoshi
# sudo apt-get install -y build-essential python
# sudo pip install virtualenv
# virtualenv venv
# source venv/bin/activate

###git clone
git clone https://github.com/jincm/zuohaoshi_server.git server

#export first from local,not need on remote when build product environment
#pip freeze >> requirements.txt

#install from requirments
sudo apt-get install -y python-dev  && pip install -r requirements.txt

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


#mongodb
#new version not need
#$ vi /etc/hosts
#54.192.157.46 repo.mongodb.org
#sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
#echo "deb http://repo.mongodb.org/apt/ubuntu "$(lsb_release -sc)"/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list
sudo apt-get install -y redis-server nginx supervisor mongodb-server

# docker pull index.tenxcloud.com/tenxcloud/mongodb
# docker tag index.tenxcloud.com/mysql:latst mysql:latest

# Not need download and install OSS.zip,it was already put into project
# sudo apt-get install unzip
# OSS_Python_API_20150811.zip

# mongod server
start-stop-daemon --background --start --quiet --pidfile /var/run/mongodb/mongodb.pid --make-pidfile --chuid mongodb --exec
/usr/bin/mongod -- --unixSocketPrefix=/var/run/mongodb --config /etc/mongodb.conf run
# /etc/init.d/mongodb stop失败的处理，将脚本中的stop改成如下，去掉最后的pidof和exec；redis类似
start-stop-daemon --stop --quiet --user mongodb

###deploy
# Not use nginx for proxy?
# sudo cp nginx_default /etc/nginx/sites-enabled/default && sudo service nginx restart
sudo cp supervisor.conf /etc/supervisor/conf.d/supervisor.conf

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
# deploy for nodejs
mkdir -p /home/jincm/zuohaoshi/develop/
scp node-v4.4.4-linux-x64.tar root@172.17.0.7:/home/jincm/zuohaoshi/develop/
cat /root/.profile :export PATH=/home/jincm/zuohaoshi/develop/node-v4.4.4-linux-x64/bin:$PATH
#pushd /usr/local/src
#tar xzf node-v4.2.3-linux-x64.tar.gz
#ln -fs `pwd`/node-v4.2.3-linux-x64/bin/node /usr/sbin/node
#ln -fs `pwd`/node-v4.2.3-linux-x64/bin/npm /usr/sbin/npm
npm -v && node -v
pushd /home/jincm/zuohaoshi/server/chat
npm install --save express
npm install --save socket.io
#test code
git clone https://github.com/plhwin/nodejs-socketio-chat.git

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
####################################################################################
####################################################################################
####################################################################################
