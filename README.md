# Kosub api




## <font color=#008000> My building log </font>
Building with guide here: https://realpython.com/flask-by-example-part-1-project-setup/

### <font color=#FF6600> (Step.1) Virtual enviroment setting </font>
```bash
$ python3 -m venv env
$ source env/bin/activate
$ deactivate
```

### <font color=#FF6600> (Step.2) Manage with 2 Workflow : production & staging </font>
- Create heroku apps
    ```bash
    $ heroku create wordcount-pro
    $ heroku create wordcount-stage
    ```
- Add the apps to git remotes.
    ```bash
    $ git remote add pro git@heroku.com:kosub-api-pro.git
    $ git remote add stage git@heroku.com:kosub-api-stage.git
    ```
- Now can push apps live to Heroku
    ```bash
    $ git push stage master
    $ git push pro master
    ```

- Config settings (different py Class) set in `config.py`
  `ProductionConfig`, `StagingConfig`, `DevelopmentConfig`, `TestingConfig`

- `APP_SETTINGS` initialize
 > to know which workflow to switch, which would be decleared individually on Local, on Heroku stage, or Heroku pro app.
 - in flask `app.py`
   ```python
   app = Flask(__name__)
   app.config.from_object(os.environ['APP_SETTINGS'])
   ```

### <font color=#800000> (Step.2-2) Local Settings </font>
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

### <font color=#800000> (Step.2-3) Heroku Settings </font>
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
