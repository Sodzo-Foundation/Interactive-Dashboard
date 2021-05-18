# Intelligent Real Time Data Visualization Dashboard (The Lawuna Project)
![N|Solid](https://i.imgur.com/yPym6k6.png)
# Intelligent Real Time Data Visualization Dashboard (The Lawuna Project)

This dashboard is meant to be used by sodzo Foundation limited to monitor water pollutants in real time: Pollutants include bottles, polythene bags, pampers and so on.


The dashboard is implemented using python django framework and [leaflets](https://leafletjs.com/).
There is a python script used to remove duplicate images using hashing algorithm as well. (Purpose not intended here)
## Usage
It's best to install Python projects in a Virtual Environment. Once you have set up a VE, clone this project

```bash
git clone  https://github.com/Sodzo-Foundation/lawuna-Interactive-Dashboard.git
```
Then

```bash
cd lawuna-Interactive-Dashboard
```
Run

```python
pip install -r requirements.txt #install required packages
python manage.py migrate # run first migration
python manage.py runserver # run the server
```
Then locate http://127.0.0.1:8000/


## License
GPL-3.0

## Actively under development


