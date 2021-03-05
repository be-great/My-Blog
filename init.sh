
export PYTHONDONTWRITEBYTECODE=1

if [ ! -d "venv" ]; then
    echo --------------------
    echo Creating virtualenv
    echo --------------------
    virtualenv venv
fi
source venv/bin/activate

pip install -r requirements.txt
export FLASK_APP=main.py
if [ ! -d "migrations" ]; then
    echo --------------------
    echo init migration folder \(create\)
    echo --------------------
    export FLASK_APP=main.py;flask db init
fi

if [ ! -d "DB" ]; then
    echo --------------------
    echo DB folder \(create\)
    echo --------------------
    mkdir DB
fi
echo --------------------
echo Generating migration DDL code
echo --------------------
flask db migrate
flask db upgrade
python test_data.py
flask run
