echo "at gunicorn.sh"
cd /var/lib/jenkins/workspace/career_backend
source venv/bin/activate


echo "$PWD"
echo "Migrations started" 
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic -- no-input

python manage.py runserver