if [ ! -d "venv" ]; then
    virtualenv -p python3.6 venv
fi

source venv/bin/activate
pip install -r requirements.txt
python main.py
deactivate
