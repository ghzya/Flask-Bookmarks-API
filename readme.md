# Flask API Bookmarks

## How to run
- Create python environtment 
```
python -m venv venv
```
- Run the environtment
```
.\venv\Scripts\Activate.ps1
```
- Install the requirements
```
pip install -r requirements.txt
```
- Run flask server
```
flask run
```

## Database setup
Run flask shell with `flask shell`
The command below must be run in flask shell that is running in python environment
- Create all table
```
from src.database import db
db.create_all()
db
```
- Delete all table
```
db.drop_all()
db
```

The default port is 5000