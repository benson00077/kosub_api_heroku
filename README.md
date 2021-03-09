# Kosub api




## My building log
Building with guide here: https://realpython.com/flask-by-example-part-1-project-setup/

#### Virtual enviroment setting
```bash
$ python3 -m venv env
$ source env/bin/activate
$ deactivate
```

#### Manage with 2 Workflow : production & staging
1. Create heroku apps
```bash
$ heroku create wordcount-pro
$ heroku create wordcount-stage
```
2. Add the apps to git remotes.
```bash
$ git remote add pro git@heroku.com:kosub-api-pro.git
$ git remote add stage git@heroku.com:kosub-api-stage.git
```
and can push apps live to Heroku
```basg
$ git push stage master
$ git push pro master
```

3. Config settings (different py Class) set in `config.py`
- ProductionConfig
- StagingConfig
- DevelopmentConfig
- TestingConfig

4. `APP_SETTINGS` to know which workflow to switch, which would be decleared individually on Local, on Heroku stage, or Heroku pro app.
 - In flask app.py
 ```bash
 app = Flask(__name__)
 app.config.from_object(os.environ['APP_SETTINGS'])
 ```

#### Local Settings
To make sure `APP_SETTINGS="...."` commands be decleared automaticaaly.
1. python module `autoenv` installed in global.
2. `.env` file add the following:
```bash
$ source env/bin/activate
$ export APP_SETTINGS="config.DevelopmentConfig"
```
3. Update then refresh my `.bashrc`
```bash
$ echo "source `which activate.sh`" >> ~/.bashrc
$ source ~/.bashrc
```
> Now, when cd into dir, the virtual environment will automatically be started and the APP_SETTINGS variable is declared. <br />
> ps. 1st time cd into dir would look like
```bash
autoenv:
autoenv: WARNING:
autoenv: This is the first time you are about to source /Users/.../myproject/.env:
autoenv:
autoenv:     --- (begin contents) ---------------------------------------
autoenv:     source env/bin/activate
autoenv:     export APP_SETTING="config.DevelopmentConfig"autoenv:
autoenv:     --- (end contents) -----------------------------------------
autoenv:
autoenv: Are you sure you want to allow this? (y/N)
```
#### Heroku Settings
- For staging:
```bash
heroku config:set APP_SETTINGS=config.StagingConfig --remote stage
```
- For production:
```bash
heroku config:set APP_SETTINGS=config.ProductionConfig --remote pro
```

##### (ref) check remote brance
 - `git remote`
 - `git remote -v`
 - `git remote rm pro` to remove pro brance
