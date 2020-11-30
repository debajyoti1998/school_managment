### install virtual environment
virtualenv myenv


### activate virtual enironment
source ./myenv/Scripts/activate



### Deactivate the virtual environment 
deactivate





### install all dependencies from requirements.txt 
pip install -r requirements.txt 

### save all dependencies in requirements.txt 
pip freeze > requirements.txt




### git first upload

git init

git add .

git commit -m "first commit"

git branch -M main

git remote add origin https://github.com/debajyoti1998/flask-basic-1.git

git push -u origin main


### new code update

git add .

git commit -m "..........."

git push -u origin main