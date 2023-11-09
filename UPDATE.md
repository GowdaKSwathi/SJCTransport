1. Deactivate site enabled for nginx
```
sudo rm /etc/nginx/sites-enabled/example.com.conf
```

2.```sudo systemctl reload nginx```

3.```sudo systemctl daemon-reload```

4.Create Virtualenv and activate

vitualenv venv

source venv/bin/activate


5.apply maigrations

```
python3 manage.py makemigrations

python3 manage.py migrate

python3 manage.py createsuperuser

python3 manage.py collectstatic
```


6.```gunicorn --bind 0.0.0.0:8000 transportproject.wsgi```

7deactivate virtualenv 


8.```chown -R www-data: /home/TransportProject/static```

9.```sudo ln -s /etc/nginx/sites-available/transport /etc/nginx/sites-enabled/```

9.1 ```sudo systemctl reload nginx```

```
10.sudo systemctl restart gunicorn.socket
11.sudo systemctl restart gunicorn.service
12.sudo systemctl status gunicorn.service
```

13.sudo systemctl daemon-reload

14.sudo systemctl restart redis.service
15.sudo systemctl status redis.service

16.systemctl restart daphne.service
17.systemctl status daphne.service

18.systemctl status customboot.service
