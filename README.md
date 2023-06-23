# Puretalk-Dashboard
## Stack Overview
![Stack Overview](https://dashboard.puretalk.ai/static/img/stack-sm.jpg?v=1)
## Diagram
![Layout](https://miro.medium.com/max/1400/1*zGC7qRcsw4G9I9u9KjMqaQ.png)
### Layout
#### /ROUTES
The routes folder hosts all the blueprint files that define all web routes. Flask uses a concept of blueprints for making application components and supporting common patterns within an application or across applications. Blueprints can greatly simplify how large applications work and provide a central means for Flask extensions to register operations on applications.
#### /STATIC
Folder that stores all static content for the webserver
#### /TEMPLATES
Folder that stores all of the HTML templates to be rendered by the Flask app
#### wsgi.py
WSGI is the python app that spins up the Flask server
#### app.py
This is the main controller that sets up the blueprint routes and libraries necessary for the dashboard to run. It also acts as main blueprint for the dashboard and renders all HTML templates
#### aggrFunctions.py
This library simplifies making aggregate searches to MongoDB
#### pureAPI.py
This blueprint holds all general API endpoints used by the dashboard itself
#### univFuncs.py
Holds all universal functions that are used throughout the app
## Definitions
### JINJA
Jinja is a fast, expressive, extensible templating engine. Special placeholders in the template allow writing code similar to Python syntax. Then the template is passed data to render the final document.
### NGINX
NGINX, is an open-source web server that is also used as a reverse proxy, HTTP cache, and load balancer.
### GUNICORN
Green Unicorn (Gunicorn) is a Python WSGI server that runs Python web application code. Gunicorn is one of many WSGI server implementations, but it’s particularly important because it is a stable, commonly-used part of web app deployments that’s powered some of the largest Python-powered web applications , such as Instagram
### HOW NGINX, GUNICORN, and FLASK work together
Nginx is at the outermost tier of the Backend(3-tiers). Middle tier is the Gunicorn and third tier is the python app which ultimately connects to the database.
Nginx is used as proxy, reverse proxy, load balancer, static data dispatcher and cache etc. While Gunicorn is the Interface between the nginx server and the python app so that the app(or any python framework) understands the incoming requests and process them accordingly.
## Setup
- Digital Ocean
  - Two servers (ubuntu-nginx-2-nyc1 and ubuntu-nginx-3-nyc1)
  - Load balancer (nyc1-load-balancer-puretalk-dashboard)

## Installation
### NGINX Install
#### Installing NGINX
* Since Nginx is available in Ubuntu’s default repositories, it is possible to install it from these repositories using the apt packaging system. Since this may be your first interaction with the apt packaging system in this session, update the local package index so that you have access to the most recent package listings. Afterward, you can install nginx:
```bash
sudo apt update
sudo apt install nginx
```
#### Firewall Adjustment
* Before testing Nginx, the firewall software needs to be adjusted to allow access to the service. Nginx registers itself as a service with ufw upon installation, making it straightforward to allow Nginx access. It is recommended that you enable the most restrictive profile that will still allow the traffic you’ve configured. Since you haven’t configured SSL for your server yet in this guide, you’ll only need to allow traffic on port 80. You can enable this by typing the following:
```bash
sudo ufw allow 'Nginx HTTP'
```
* Verify the change
```bash
sudo ufw status
```
* Verify NGINX status
```bash
systemctl status nginx
```
### Flask with GUNICORN
#### Installing Components
* The first step is to install all of the necessary packages from the default Ubuntu repositories. This includes pip, the Python package manager, which will manage your Python components. You’ll also get the Python development files necessary to build some of the Gunicorn components. First, update the local package:
```bash
sudo apt update
```
* Then install the packages that will allow you to build your Python environment. These include python3-pip, along with a few more packages and development tools necessary for a robust programming environment:
```bash
sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
```
* With these packages in place, move on to creating a virtual environment for your project.
#### Setting up Python Virtual Environment
* Next, set up a virtual environment to isolate your Flask application from the other Python files on the system. Start by installing the python3-venv package, which will install the venv module:
```bash
sudo apt install python3-venv
cd /var/www
mkdir puretalk-dashboard
cd puretalk-dashboard
```
* Create a virtual environment
```bash
python3 -m venv puretalk-dashboard-env
```
* Activate the source
```bash
source puretalk-dashboard-env/bin/activate
```
* Clone Repo
```bash
git clone https://github.com/meca-technologies/Puretalk-Dashboard.git
```
* Install all requirements
```bash
pip install -r requirements.txt
```
* You can test the webserver by running
```bash
gunicorn --bind 0.0.0.0:5000 wsgi:app
```
* Output should look like this
```
Output
[2021-11-19 23:07:57 +0000] [8760] [INFO] Starting gunicorn 20.1.0
[2021-11-19 23:07:57 +0000] [8760] [INFO] Listening at: http://0.0.0.0:5000 (8760)
[2021-11-19 23:07:57 +0000] [8760] [INFO] Using worker: sync
[2021-11-19 23:07:57 +0000] [8763] [INFO] Booting worker with pid: 8763
[2021-11-19 23:08:11 +0000] [8760] [INFO] Handling signal: int
[2021-11-19 23:08:11 +0000] [8760] [INFO] Shutting down: Master
```
#### Setting up GUNICORN
* Start by deactivating the virtual environment
```bash
deactivate
```
* Create a unit file ending in .service within the /etc/systemd/system directory to begin:
```bash
sudo nano /etc/systemd/system/puretalk-dashboard.service
```
* Inside paste the following and save the file:
```bash
[Unit]
Description=Gunicorn instance to serve puretalk dashboard
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/puretalk-dashboard
Environment="PATH=/var/www/puretalk-dashboard/puretalk-dashboard-env/bin"
ExecStart=/var/www/puretalk-dashboard/puretalk-dashboard-env/bin/gunicorn --workers 10 --bind unix:myproject.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target
```
* Now we can start the service
```bash
sudo systemctl start puretalk-dashboard
```
* Then enable it so that it starts at boot:
```bash
sudo systemctl enable puretalk-dashboard
```
* Check the status:
```bash
sudo systemctl status puretalk-dashboard
```
* The output for above should be similar to this
```bash
● puretalk-dashboard.service - Gunicorn instance to serve myproject
   Loaded: loaded (/etc/systemd/system/puretalk-dashboard.service; enabled; vendor preset
   Active: active (running) since Fri 2021-11-19 23:08:44 UTC; 6s ago
 Main PID: 8770 (gunicorn)
    Tasks: 10 (limit: 1151)
   CGroup: /system.slice/puretalk-dashboard.service
       	├─9291 /var/www/puretalk-dashboard/puretalk-dashboard-env/bin/python3.6 /var/www/puretalk-dashboard/puretalk-dashboard-env/bin/gunicorn --workers 3 --bind unix:puretalk-dashboard.sock -m 007 wsgi:app
       	├─9309 /var/www/puretalk-dashboard/puretalk-dashboard-env/bin/python3.6 /var/www/puretalk-dashboard/puretalk-dashboard-env/bin/gunicorn --workers 3 --bind unix:puretalk-dashboard.sock -m 007 wsgi:app
       	├─9310 /var/www/puretalk-dashboard/puretalk-dashboard-env/bin/python3.6 /var/www/puretalk-dashboard/puretalk-dashboard-env/bin/gunicorn --workers 3 --bind unix:puretalk-dashboard.sock -m 007 wsgi:app
       	└─9311 /var/www/puretalk-dashboard/puretalk-dashboard-env/bin/python3.6 /var/www/puretalk-dashboard/puretalk-dashboard-env/bin/gunicorn --workers 3 --bind unix:puretalk-dashboard.sock -m 007 wsgi:app
…
```
#### Configuring NGINX
* Begin by creating a new server block configuration file in Nginx’s sites-available directory. We’ll call this puretalk-dashboard to stay consistent with the rest of the guide:
```bash
sudo nano /etc/nginx/sites-available/puretalk-dashboard
```
* Paste:
```bash
server {
    listen 80;
    server_name dashboard.puretalk.ai www.dashboard.puretalk.ai;

    client_max_body_size 100M;

    proxy_headers_hash_max_size 512;
    proxy_headers_hash_bucket_size 128;

    location / {
        include proxy_params;
        proxy_set_header        X-Real-IP         $remote_addr;
        proxy_set_header        X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_pass http://unix:/var/www/puretalk-dashboard/puretalk-dashboard.sock;
    }

    location /leads/generator/ {
        include proxy_params;
        proxy_set_header        X-Real-IP         $remote_addr;
        proxy_set_header        X-Forwarded-For   $proxy_add_x_forwarded_for;
        add_header 'Access-Control-Allow-Origin' '*' always;
        add_header 'Access-Control-Allow-Methods' 'POST' always;
        add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range' always;
        add_header 'Access-Control-Expose-Headers' 'Content-Length,Content-Range' always;
        proxy_pass http://unix:/var/www/puretalk-dashboard/puretalk-dashboard.sock;
    }
}
```
* To enable the Nginx server block configuration you’ve created, link the file to the "sites-enabled" directory. You can do this by running the ln command and the -s flag to create a symbolic or soft link, as opposed to a hard link:
```bash
sudo ln -s /etc/nginx/sites-available/puretalk-dashboard /etc/nginx/sites-enabled
```
* Test for syntax errors
```bash
sudo nginx -t
```
* If there are no issues restart NGINX
```bash
sudo systemctl restart nginx
```
* Allow full to the NGINX server:
```bash
sudo ufw allow 'Nginx Full'
```

### Commands
```bash
cd /var/www/myproject
source myprojectenv/bin/activate
sudo systemctl start myproject.service
```
