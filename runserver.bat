cd API
start cmd.exe @cmd /k "python main.py"
cd ..
cd Burger
start cmd.exe @cmd /k "python manage.py runserver 0.0.0.0:8000"