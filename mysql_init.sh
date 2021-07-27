sudo /etc/init.d/mysql start
mysql -u root -e "drop database if exists qa;"
mysql -u root -e "create database qa;"
mysql -u root -e "create user 'aci30'@'localhost' identified by 'aci30';"
mysql -u root -e "grant all privileges on qa.* to 'aci30'@'localhost';"
mysql -u root -e "flush privileges;"
echo "mysql init done"