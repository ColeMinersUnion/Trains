# Trains
## Getting Started
To start a virtual environment. This should be pre-installed with python. 
```bash
python3 -m venv env
```
### MacOS or Linux
```bash
source env/bin/activate
```
### Windows
```
env\Scripts\activate
```

## Dependency Managament
```bash
pip install -r requirements.txt
```
Whenever you add a new package: 
```bash
pip freeze > requirements.txt
```

```python
SpeedLimits = [70, 70, 70, 70, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 70, 70, 70, 70, 70, 70, 70, 70, 70, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 70, 70, 70, 70, 70, 70, 70, 70, 70, 26, 28, 28, 28, 28, 28, 28, 28, 28, 30, 30, 30, 30, 30, 30, 30, 15, 15, 15, 15, 15, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 30, 30, 70, 70, 70, 70, 70, 70, 60, 60, 60, 60, 70, 70, 70, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 70, 70, 70, 60, 60, 60, 60, 70, 70, 70, 70, 70, 70, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30]
```
