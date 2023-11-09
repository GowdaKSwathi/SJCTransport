Step 1 - Installing python and nginx
Let's update the server's package index using the command below:

OR follow 

https://github.com/mitchtabian/HOWTO-django-channels-daphne

```
sudo apt update
sudo apt install python3-pip python3-dev nginx
```
This will install python, pip and nginx server


Step 2 - Creating a python virtual environment
```sudo pip3 install virtualenv```
This will install a virtual environment package in python. Let's create a project directory to host our Django application and create a virtual environment inside that directory.

```
mkdir ~/projectdir
cd ~/projectdir
virtualenv env
```
A virtual environment named env will be created. Let's activate this virtual environment:

```source env/bin/activate```
Step 3 - Installing Django and gunicorn in vitualenv
```pip install django gunicorn```
This installs Django and gunicorn in our virtual environment

Step 4 - Setting up our Django project
At this point you can either copy your existing Django project into the projectdir folder or create a fresh one as shown below:

django-admin startproject textutils ~/projectdir
Add your IP address or domain to the ALLOWED_HOSTS variable in settings.py.

If you have any migrations to run, perform that action:

```
python3 manage.py makemigrations

python3 manage.py migrate

python3 manage.py createsuperuser

python3 manage.py collectstatic
```
Let's test this sample project by running the following commands this is not recommended:

```sudo ufw allow 8000```
This opens port 8000 by allowing it over the firewall. Let's start our Django development server to test the setup so far:

~/projectdir/manage.py runserver 0.0.0.0:8000

Step 5 - Configuring gunicorn
Lets test gunicorn's ability to serve our application by firing the following commands:

```gunicorn --bind 0.0.0.0:8000 transport.wsgi```

This should start gunicorn on port 8000. We can go back to the browser to test our application. Visiting http://<ip-address>:8000 shows a page like this:

Deactivate the virtualenvironment by executing the command below:

deactivate
Let's create a system socket file for gunicorn now:

```sudo vim /etc/systemd/system/gunicorn.socket```
Paste the contents below and save the file

```
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```
Next, we will create a service file for gunicorn

```sudo vim /etc/systemd/system/gunicorn.service```
Paste the contents below inside this file:

```
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/home/TransportWeb
ExecStart=/home/TransportWeb/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          transportproject.wsgi:application

[Install]
WantedBy=multi-user.target
```
Lets now start and enable the gunicorn socket

```
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
```
Step 6 - Configuring Nginx as a reverse proxy
Create a configuration file for Nginx using the following command

```sudo vim /etc/nginx/sites-available/transport```
Paste the below contents inside the file created

```
server {
    listen 80;
    server_name transport.sjcit.ac.in;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/TransportWeb;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
    
    location /ws/ {
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_redirect off;
        proxy_pass http://127.0.0.1:8001;
    }
}
```

Note1: If you don not want to serve websocket then ```location /ws/``` remove.
Activate the configuration using the following command:

```sudo ln -s /etc/nginx/sites-available/transport /etc/nginx/sites-enabled/
```
Restart nginx and allow the changes to take place.

```sudo systemctl restart nginx```

# DEBUGGING

Here are some commands you can use to look at the server logs. **These commands are absolutely crucial to know.** If your server randomly isn't working one day, this is what you use to start debugging.

1. `sudo journalctl` is where all the logs are consolidated to. That's usually where I check.
1. `sudo tail -F /var/log/nginx/error.log` View the last entries in the error log
1. `sudo journalctl -u nginx` Nginx process logs
1. `sudo less /var/log/nginx/access.log` Nginx access logs
1. `sudo less /var/log/nginx/error.log` Nginx error logs
1. `sudo journalctl -u gunicorn` gunicorn application logs
1. `sudo journalctl -u gunicorn.socket` check gunicorn socket logs

# Install and Setup Redis For ASGI (Django Channels)

Redis is used as a kind of "messaging queue" for django channels. Read more about it here [https://channels.readthedocs.io/en/stable/topics/channel_layers.html?highlight=redis#redis-channel-layer](https://channels.readthedocs.io/en/stable/topics/channel_layers.html?highlight=redis#redis-channel-layer)

`sudo apt install redis-server`

Navigate to `/etc/redis/`

open `redis.conf`

`CTRL+F` to find 'supervised no'

change 'supervised no' to 'supervised systemd'

`SAVE`

`sudo systemctl restart redis.service`

`sudo systemctl status redis`

Should see this:

<div class="row  justify-content-center">
  <img class="img-fluid text-center" src = "https://github.com/mitchtabian/HOWTO-django-channels-daphne/blob/master/images/redis_status.PNG">
</div>
<br>

`CTRL+C` to exit.

`sudo apt install net-tools`

Confirm Redis is running at 127.0.0.1. Port should be 6379 by default.

`sudo netstat -lnp | grep redis`

`sudo systemctl restart redis.service`

# ASGI for Hosting Django Channels as a Separate Application

From the Django channels docs:

> ASGI (Asynchronous Server Gateway Interface), is the specification which Channels are built upon, designed to untie Channels apps from a specific application server and provide a common way to write application and middleware code.

`su django`

Create file named `asgi.py` in `/home/django/CodingWithMitchChat/src/CodingWithMitchChat` with this command:

`cat > asgi.py` 'django' must be the owner of this file.

Paste in the following:

```
"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
"""

import os
import django
from decouple import config
from channels.routing import get_default_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", f'{config("PROJECT_NAME")}.settings')
django.setup()
application = get_default_application()

```

`CTRL+D` to save.

You can open the file to confirm everything looks good.

`ls -l` to check ownership. `django` needs to be the owner.

<div class="row  justify-content-center">
  <img class="img-fluid text-center" src = "https://github.com/mitchtabian/HOWTO-django-channels-daphne/blob/master/images/CodingWithMitchChat_ownership.PNG">
</div>
<br>

# Deploying Django Channels with Daphne & Systemd

Gunicorn is what we use to run the WSGI application - which is our django app. To run the ASGI application we need something else, an additional tool. **[Daphne](https://github.com/django/daphne)** was built for Django channels and is the simplest. We can start daphne using a systemd service when the server boots, just like we start gunicorn and then gunicorn starts the django app.

Here are some references I found helpful. The information on this is scarce:

1. [https://channels.readthedocs.io/en/latest/deploying.html](https://channels.readthedocs.io/en/latest/deploying.html)
1. [https://stackoverflow.com/questions/50192967/deploying-django-channels-how-to-keep-daphne-running-after-exiting-shell-on-web](https://stackoverflow.com/questions/50192967/deploying-django-channels-how-to-keep-daphne-running-after-exiting-shell-on-web)

`su root`

`apt install daphne`

Navigate to `/etc/systemd/system/`

Create `daphne.service`. Notice the port is `8001`. This is what we need to use for our `WebSocket` connections in the templates.

```
[Unit]
Description=WebSocket Daphne Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/home/django/CodingWithMitchChat/src
ExecStart=/home/django/CodingWithMitchChat/venv/bin/python /home/django/CodingWithMitchChat/venv/bin/daphne -b 0.0.0.0 -p 8001 CodingWithMitchChat.asgi:application
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

`systemctl daemon-reload`

`systemctl start daphne.service`

`systemctl status daphne.service`

You should see something like this. If you don't, go back and redo this section. Check that your filepaths are all **exactly the same as mine in `daphne.service`**. That is the #1 reason people have issues.

<div class="row  justify-content-center">
  <img class="img-fluid text-center" src = "https://github.com/mitchtabian/HOWTO-django-channels-daphne/blob/master/images/daphe_status.PNG">
</div>
<br>

`CTRL+C`

# Starting the daphne Service when Server boots

With gunicorn and the WSGI application, we created a `gunicorn.socket` file that tells gunicorn to start when the server boots (at least this is my understanding). I couldn't figure out how to get this to work for daphne so instead I wrote a bash script that will run when the server boots.

#### Create the script to run daphne

Navigate to `/root`

create `boot.sh`

```
#!/bin/sh
sudo systemctl start daphne.service
```

Save and close.

Might have to enable it to be run as a script (not sure if this is needed)
`chmod u+x /root/boot.sh`

If you want to read more about shell scripting, I found this helpful:
[https://ostechnix.com/fix-exec-format-error-when-running-scripts-with-run-parts-command/](https://ostechnix.com/fix-exec-format-error-when-running-scripts-with-run-parts-command/).

#### Tell systemd to run the bash script when the server boots

Navigate to `/etc/systemd/system`

create `on_boot.service`

```
[Service]
ExecStart=/root/boot.sh

[Install]
WantedBy=default.target
```

Save and close.

`systemctl daemon-reload`

##### Start it

`sudo systemctl start on_boot`

##### Enable it to run at boot

`sudo systemctl enable on_boot`

##### Allow daphne service through firewall

`ufw allow 8001`

##### Restart the server

`sudo shutdown -r now`

##### Check the status of `on_boot.service`

`systemctl status on_boot.service`

Should see this. If not, check logs: `sudo journalctl -u on_boot.service`

<div class="row  justify-content-center">
  <img class="img-fluid text-center" src = "https://github.com/mitchtabian/HOWTO-django-channels-daphne/blob/master/images/on_boot_service_status.PNG">
</div>
<br>

##### Check if the daphne service started when the server started:

`systemctl status daphne.service`

Should see this. If not, check logs: `sudo journalctl -u daphne.service`

<div class="row  justify-content-center">
  <img class="img-fluid text-center" src = "https://github.com/mitchtabian/HOWTO-django-channels-daphne/blob/master/images/daphne_service_status.PNG">
</div>
<br>

#### Where are the logs?

journalctl is my general go-to. You can filter specifically for a service like this:

```
sudo journalctl -u on_boot.service // for on_boot.service
sudo journalctl -u daphne.service // for daphne.service
```

# Domain Setup

If you want a custom domain name (which probably everyone does), this section will take you through how to do that.

#### Purchasing a domain

I like to use [namecheap.com](https://www.namecheap.com/) but it doesn't matter where you buy it from.

#### Point DNS to Digital Ocean

On the home screen, click the "manage" button on the domain you purchased.

<div class="row  justify-content-center">
  <img class="img-fluid text-center" src = "https://github.com/mitchtabian/HOWTO-django-channels-daphne/blob/master/images/namecheap_home.PNG">
</div>
<br>

In the "nameservers" section, select "custom DNS" and point to digital ocean.

<div class="row  justify-content-center">
  <img class="img-fluid text-center" src = "https://github.com/mitchtabian/HOWTO-django-channels-daphne/blob/master/images/nameservers.PNG">
</div>
<br>

#### Add the Domain in Digital Ocean

Select your project in digital ocean and click "add domain" on the right.

<div class="row  justify-content-center">
  <img class="img-fluid text-center" src = "https://github.com/mitchtabian/HOWTO-django-channels-daphne/blob/master/images/add_a_domain.PNG">
</div>
<br>

Fill in your domain name.

<div class="row  justify-content-center">
  <img class="img-fluid text-center" src = "https://github.com/mitchtabian/HOWTO-django-channels-daphne/blob/master/images/add_a_domain_1.PNG">
</div>
<br>

Add the following DNS records. Replace `open-chat.xyx` with your domain name. And you can ignore the CDN.

<div class="row  justify-content-center">
  <img class="img-fluid text-center" src = "https://github.com/mitchtabian/HOWTO-django-channels-daphne/blob/master/images/dns_records.PNG">
</div>
<br>

#### Update Nginx config

Earlier we configured Nginx to proxy pass to gunicorn. We need to add the new domain to that configuration.

visit `/etc/nginx/sites-available`

Update `CodingWithMitchChat`

```
server {
    server_name 157.245.134.6 open-chat-demo.xyz www.open-chat-demo.xyz;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/django/CodingWithMitchChat/src;
    }

     location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

`sudo systemctl reload nginx`

Make sure nginx configuration is still good.

`sudo nginx -t`

#### Update `ALLOWED_HOSTS`

Navigate to `/home/django/CodingWithMitchChat/src/CodingWithMitchChat/`

Update `settings.py` with the domain you purchased. Also make sure your ip is correct.

```
ALLOWED_HOSTS = ["157.245.134.6", "open-chat-demo.xyz", "www.open-chat-demo.xyz"]
```

Apply the changes

`service gunicorn restart`

## TIME TO WAIT...

It can take some time to see your website available at the custom domain. I don't really know how long this will actually take. I waited about an hour and it was working for me.

#### How do you know it's working?

Visiting your domain you should see this **OR you should see your project live and working**.

<div class="row  justify-content-center">
  <img class="img-fluid text-center" src = "https://github.com/mitchtabian/HOWTO-django-channels-daphne/blob/master/images/welcome_to_nginx.PNG">
</div>
<br>

# HTTPS (If you have a domain registered and it's working)

**Do not do this step unless you're able to visit your website using the custom domain.** See [How do you know it's working?](How-do-you-know-its-working?)

#### Install certbot

HTTPS is a little more difficult to set up when using Django Channels. Nginx and Daphne require some extra configuring.

`sudo apt install certbot python3-certbot-nginx`

`sudo systemctl reload nginx`

Make sure nginx configuration is still good.

```
sudo nginx -t
```

#### Allow HTTPS through firewall

`sudo ufw allow 'Nginx Full'`

`sudo ufw delete allow 'Nginx HTTP'` Block standard HTTP

#### Obtain SSL certificate

`sudo certbot --nginx -d <your-domain.whatever> -d www.<your-domain.whatever>`

For me:

```
sudo certbot --nginx -d open-chat-demo.xyz -d www.open-chat-demo.xyz
```

#### Verifying Certbot Auto-Renewal

`sudo systemctl status certbot.timer`

#### Test renewal process

`sudo certbot renew --dry-run`

You should see this

<div class="row  justify-content-center">
  <img class="img-fluid text-center" src = "https://github.com/mitchtabian/HOWTO-django-channels-daphne/blob/master/images/verify_certbot.PNG">
</div>
<br>

#### Update CORS in digital ocean

Update for HTTPS in spaces settings

<div class="row  justify-content-center">
  <img class="img-fluid text-center" src = "https://github.com/mitchtabian/HOWTO-django-channels-daphne/blob/master/images/CORS.PNG">
</div>
<br>

#### Update settings.py

Set `BASE_URL` variable in `settings.py` to your domain name.

## Update nginx config

We need to tell nginx to allow websocket data to move through port 8001. I'm not really sure how to explain this. I don't understand it fully. Similar to how we allow gunicorn to proxy pass nginx.

Navigate to `/etc/nginx/sites-available`

Update `CodingWithMitchChat`

```
server {

    ...

    location /ws/ {
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_redirect off;
        proxy_pass http://127.0.0.1:8001;
    }

    ...
}
```

## Update `daphne.service`

Tell daphne how to access our https cert.

Navigate to `/etc/systemd/system`

Update `daphne.service`

```
[Unit]
Description=WebSocket Daphne Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/home/django/CodingWithMitchChat/src
ExecStart=/home/django/CodingWithMitchChat/venv/bin/python /home/django/CodingWithMitchChat/venv/bin/daphne -e ssl:8001:privateKey=/etc/letsencrypt/live/open-chat-demo.xyz/privkey.pem:certKey=/etc/letsencrypt/live/open-chat-demo.xyz/fullchain.pem CodingWithMitchChat.asgi:application
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

# Create a superuser

Before you test the server create a superuser.

`su django`

`cd /home/django/CodingWithMitchChat/`

`source venv/bin/activate`

`cd src`

`python manage.py createsuperuser`

# Finishing up

Restart the server and visit your website to try it out. Everything should be working now.

**If you followed my course remember to create a public chat room from the admin with the title "General".**

Thanks for reading and feel free to contribute to this document if you have a better way of explaining things. I am by no means a web expert.

# FAQ

Here are some things I wish I knew when doing this for the first time.

### If you change a file or pull a code update to the project, do you need to do anything?

Yes.

If you only change code that is _not related to django channels_ then you only need to run `service gunicorn restart`.

But if you change any code related to django channels, **then you must also restart the daphne service**: `service daphne restart`.

To be safe, I always just run both. It can't hurt.

```
service gunicorn restart
service daphne restart
```


<br>

### Service Status Errors

Throughout this document we periodically check the status of the services that we set up. Things like:

1. `sudo systemctl status gunicorn`
1. `sudo systemctl status redis`
1. `systemctl status daphne.service`
1. `systemctl status on_boot.service`
1. `sudo systemctl status certbot.timer`

If any of these fail, it's not going to work and you've done something wrong. The most common problem is the directory structure does not match up. For example you might use `/home/django/django_project/src/` instead of `/home/django/CodingWithMitchChat/src/`. You need to look very carefully at your directory structures and make sure the naming is all correct and correlates with the `.service` files you build.

When you make a change to a `.service` file, **Always run `sudo systemctl daemon-reload`**. Or to be safe, just restart the damn server `sudo shutdown -r now`. Restarting the server is the safe way, but also the slowest way.

### CORS error in web console

You are getting an error in web console saying: "No 'Access-Control-Allow-Origin' header is present on the requested resource".

Fix this by adding CORS header in spaces settings.
See [This image](https://github.com/mitchtabian/HOWTO-django-channels-daphne/blob/master/images/CORS.PNG) for the configuration.



#Create supervisor config fiel fro background task like celery worker and beat

1.https://www.codingforentrepreneurs.com/blog/hello-linux-celery-supervisor/

```
sudo apt-get update -y

sudo apt-get install supervisor -y 

sudo service supervisor start
```

2. your All supervisor proccesses go in following path
```
/etc/supervisor/conf.d/
```
So, if you ever need to add a new process, you'll just add it there.

Let's create our project's celery configuration file for supervisor.

Copy
```
touch /etc/supervisor/conf.d/myproject-celery-worker.conf
```

Now you should see:

Copy
$ ls -al /etc/supervisor/conf.d/
myproject-celery-worker.conf

and commamd is below

```
[program:transport_celery_worker]
user=root
directory=/home/TransportWeb
command=/home/TransportWeb/venv/bin/celery -A transportproject.celery worker -l info

autostart=true
autorestart=true
stdout_logfile=/home/TransportWeb/celery/celery.log
stderr_logfile=/home/TransportWeb/celery/celery.err.log
```

for celery beat create new conf file like myproject-celery-beat.conf

```
[program:transport_celery_beat]
user=root
directory=/home/TransportWeb
command=/home/TransportWeb/venv/bin/celery -A transportproject beat -l info

autostart=true
autorestart=true
stdout_logfile=/home/TransportWeb/celery/beat/celery.log
stderr_logfile=/home/TransportWeb/celery/beat/celery.err.log
```
Let's break it down line by line.

[program:myproject_celery]: the myproject_celery is the name of the supervisor process. Naturally, myproject_celery is an arbitrary name. Once we complete Step 5, you'll be able to run the following commands:

sudo supervisorctl status myproject_celery
sudo supervisorctl start myproject_celery
sudo supervisorctl stop myproject_celery
sudo supervisorctl restart myproject_celery
user=root: Set the user you want to allow access to this process. This must be set.

directory=/var/www/myproject/src/ This is the working directory for your project (notice mine has src at the end)

command=... This is the command you want your process to run. Our command is: - /var/www/myproject/bin/celery This is the recently installed celery bash command - -A myproject This is a celery argument for where your project's celery app is located. Mine is in celery.py in my main Django conf directory. (We'll add this in the next step). In my case it's src directory -> cfehome module -> celery module -> celery application - -l info This just means "log level is info" so we just get general info about this app. Check the celery docs for more log levels.

autostart Do you want this process to auto start? We do.

autorestart Do you want this process to auto restart if things fail? We do.

stdout_logfile and stderr_logfile are locations for log files. You might need to run mkdir /var/log/myproject/ to ensure these files are actually added. These log files are great for diagnosing errors.

3.Update Supervisor
```
supervisorctl reread
supervisorctl update
```
4.8. Check Our Supervisor Program/Process Status
As we mentioned when we crated the myproject_guincorn supervisor program, we can now do:

```
sudo supervisorctl status myproject_celery
```
5.A few other useful commands (again):

```
sudo supervisorctl start myproject_celery
sudo supervisorctl stop myproject_celery
sudo supervisorctl restart myproject_celery
```

Note: Do not worry supervisor autorestart after boot system






# References

1. [https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04)
1. [https://channels.readthedocs.io/en/latest/](https://channels.readthedocs.io/en/latest/)
1. [https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-20-04](https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-20-04)
1. [https://www.digitalocean.com/community/tutorials/how-to-set-up-object-storage-with-django](https://www.digitalocean.com/community/tutorials/how-to-set-up-object-storage-with-django)
1. [https://stackoverflow.com/questions/61101278/how-to-run-daphne-and-gunicorn-at-the-same-time](https://stackoverflow.com/questions/61101278/how-to-run-daphne-and-gunicorn-at-the-same-time)
1. [https://github.com/conda-forge/pygridgen-feedstock/issues/10](https://github.com/conda-forge/pygridgen-feedstock/issues/10)
1. [https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-20-04](https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-20-04)
