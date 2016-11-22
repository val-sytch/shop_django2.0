# shop_django2.0
Shop built with Mezzanine/ Cartridge

Installation:

Clone repository:
```
$ git clone https://github.com/val-sytch/shop_django2.0.git
$ cd shop_django2.0
```
Create virtualenv and activate it
```
$ virtualenv -p python3.5 venv
$ . venv/bin/activate
```
Install fabric to use shortcuts
```
$(venv) pip install Fabric3
```
Install all required packages
```
$(venv) fab install_requir
```
Open local_settings.py and local_settings_prod.py and set all variables that contain value your...

You could choose a database:

1. sqlite3 as a default/development database(do nothing)
2. MySQL for production. To use it set the environment variable:
```
$(venv)export DJANGO_PROJ_MODE=prod
```
Create database(pay attention to superuser credentials)
```
$(venv) fab initdb
```
Additional info: to switch to default sqlite db just unset
the env variable and launch db initialising once again
```
$(venv)unset DJANGO_PROJ_MODE=prod
$(venv) fab initdb
```
Optionally(fill in database with Products)
```
$(venv) fab download_img
```
Run server
```
$(venv) fab runserver
```
Go to http://127.0.0.1:8000/admin/, Log in with superuser credendials, go to ```Pages```, edit ```Shop```:

1. Select Products that you want to show in your shop
2. In Meta data change ```URL``` for ```/```
3. in ```Show in menus``` uncheck all parameter: ``` Top navigation bar, Left-hand tree, Footer```
