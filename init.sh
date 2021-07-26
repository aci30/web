sudo rm -f /etc/nginx/sites-enabled/default
sudo ln -sf /home/box/web/etc/nginx.conf  /etc/nginx/sites-enabled/test.conf
sudo /etc/init.d/nginx restart
#sudo ln -sf /home/box/web/etc/gunicorn.conf   /etc/gunicorn.d/test
gunicorn --bind='0.0.0.0:8080' hello:app -D
cd ask/
gunicorn --bind='0.0.0.0:8000' -w 2 --error-logfile error.log --log-level=debug ask.wsgi:application
#sudo /etc/init.d/gunicorn restart
#sudo /etc/init.d/mysql start
