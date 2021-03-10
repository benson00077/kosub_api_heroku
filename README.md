# Kosub api




# <font color=#008000> My building log </font>
Building with guide here: https://realpython.com/flask-by-example-part-1-project-setup/

## <font color=#FF6600> (Step.1) Virtual enviroment setting </font>
```bash
$ python3 -m venv env
$ source env/bin/activate
$ deactivate
```

## <font color=#FF6600> (Step.2) Manage with 2 Workflow : production & staging </font>
1. Create heroku apps
    ```bash
    $ heroku create wordcount-pro
    $ heroku create wordcount-stage
    ```
2. Add the apps to git remotes.
    ```bash
    $ git remote add pro git@heroku.com:[myapp-pro].git
    $ git remote add stage git@heroku.com:[my-app-stage].git
    # or maybe ...
    $ git remote add stage https://git.heroku.com/[myapp-pro-stage].git
    ```
3. Now can push apps live to Heroku
    ```bash
    $ git push stage master
    $ git push pro master
    ```

4. Config settings (different py Class) set in `config.py`
  `ProductionConfig`, `StagingConfig`, `DevelopmentConfig`, `TestingConfig`

5. `APP_SETTINGS` initialize
 + to know which workflow to switch, which would be decleared individually on Local, on Heroku stage, or Heroku pro app.
 +  in flask `app.py`:
   ```python
   app = Flask(__name__)
   app.config.from_object(os.environ['APP_SETTINGS'])
   ```

## <font color=#800000> (Step.2-2) Local Settings </font>
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

## (Step.2-3) Heroku Settings
- For staging:
```bash
$ heroku config:set APP_SETTINGS=config.StagingConfig --remote stage
```
- For production:
```bash
$ heroku config:set APP_SETTINGS=config.ProductionConfig --remote pro
```

- ref: check remote branch
 - `git remote`
 - `git remote -v`
 - `git remote rm pro` to remove pro brance

 ## (Step.3) db on heroku
 1. Create addons: 
 ```basg
 $ heroku addons:create heroku-postgresql:hobby-dev --app [myapp-stage]
 ```
 2. Check addons status: 
 ```bash
 $ heroku config --app [myapp-stage]
 === kosub-api-pro Config Vars
 APP_SETTINGS: config.ProductionConfig
 DATABASE_URL: postgres://...:...
 ```

 ## (Step.3-2) connect to db
 - <strike>Adds `DATABASE_URL = os.environ['DATABASE_URL']` in `config.py` parent Class.</strike> falied.
 - Adds `DATABASE_URL = os.environ['DATABASE_URL']`  in `app.py`. successed.
 - Adds `export DATABASE_URL="postgresql:///kosub_subtitles"` in `.env` file. (For loacal site access)

 ## (Step.3-3) import local sql file to heroku (SQLite -> PSQL)
 1. Dump SQLite3 and revise this `.sql` file to allign with PSQL syntax.
 2. Import the file to local PSQL `$ psql -d [my-psql-db] -U [psql-user] -W < sqlite-dump.sql `
 2. Dump local PSQL `$ pg_dump --no-owner [my-psql-db] > dump.sql`. Get output dump `.sql` files.
 3. Upload the PSQL dump file to Heroku addons `$ heroku pg:psql --app [my-app-pro] < dump.sql`.
 