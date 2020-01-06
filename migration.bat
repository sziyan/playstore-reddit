@echo off
echo "Make sure in virtualenv folder."
pause

echo "Create migration folder"

migrate create migration "Project"

set /p db=Enter database filename(with .db):

echo "Setting up version control."
python migration/manage.py version_control sqlite:///%db% migration

echo "Setting path."
migrate manage manage.py --repository=migration --url=sqlite:///%db%