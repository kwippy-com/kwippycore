README
------

Kwipppy Project, development system:

Ubuntu Linux
------------
1. We need the following dependencies installed(use apt-get):
build-essential
mysql-server-5.0
mysql-client-5.0
libmysqlclient15-dev
python2.5
python2.5-dev
subversion

2. Install easy_install from the URL below
http://peak.telecommunity.com/dist/ez_setup.py
http://pypi.python.org/pypi/setuptools  (has all the downloadable eggs etc.)
Install the following python packages using easy_install:
simplejson
MySQL-python
Imaging

3. Finally, install django from the svn provided below:
svn co http://code.djangoproject.com/svn/django/trunk/ django-trunk
go in and do 
sudo python setup.py install

4. Now run the schema building commands on the base directory
python manage.py syncdb
Then run any migrations
python migrate.py


Author
------
Dipankar Sarkar (dipankarsarkar@gmail.com)
