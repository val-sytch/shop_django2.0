from fabric.api import local


############################
# DJOG_SHOP CUSTOM COMMANDS#
############################

def runserver():
    """
    Run Django development sever
    """
    local('python manage.py runserver')


def initdb():
    """
    Create new empty db
    """
    local('python manage.py createdb --nodata')


def superuser():
    """
    Create superuser
    """
    local('python manage.py createsuperuser')


def download_img():
    """
    Launch script, which parse wiki for dog breeds, upload images and create Product(dog)
    """
    local('python manage.py download_img')


def install_requir():
    """
    Install all required packages from requirements/base.txt
    """
    local(' pip install -r requirements.txt')


def targz():
    """
    make tar.gz for distribution. It could be easily installed at other PC or server with pip
    """
    local('python setup.py sdist')
