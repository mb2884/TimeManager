@ECHO OFF
REM --------------------------------------------------------------------
REM buildandrun.bat
REM Author: Bob Dondero
REM --------------------------------------------------------------------

REM Create file .coverage
python -m coverage run timemanager.py

REM Create directory htmlcov
python -m coverage html --omit=auth.py,tasksplitter.py

REM View the results, htmlcov\index.html, using a browser
