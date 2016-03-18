cd setuptools-20.3
python ez_setup.py
easy_install pip
cd ..
pip install virtualenv
pip install virtualenvwrapper-win
mkvirtualenv megabite
workon megabite
pip install -r requirements.txt
pause