@echo off
set filename=config.ini

if exist %filename% (
    for /f "tokens=*" %%A in (%filename%) do (
        echo %%A
    )
	python manage.py runserver	
) else (
    echo Config.ini not found
)
pause