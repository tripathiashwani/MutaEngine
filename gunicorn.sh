echo "at gunicorn.sh"
source env/bin/activate

cd /var/lib/jenkins/workspace/django-cicd/app
echo "$PWD"
echo "Migrations started" 
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic -- no-input

python3 manage.py runserver