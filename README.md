source code hosted at https://github.com/JustinMaxwell/PYH-Calculator
Webapp hosted from https://www.pythonanywhere.com/user/jkmaxwell/
Webaddress: pyhcalculator.com

## Typical process includes:
1. Fork project in github.
1. `git pull` or `git clone` from github to local filesystem.
1. Start virtualenv
    1. If it's not installed `pip3 install virtualenv virtualenvwrapper`
    1. run `mkvirtualenv myvirtualenv --python=/usr/bin/python3.6`
    1. To re-activate run `workon myvirtualenv` to deativate run `deactivate`
1. pip install from requirements.txt
    1. cd into git repo directory.
    1. run `pip install -r requirements.txt`
1. Create new local branch for changes `git checkout -b <new-branch-name>`
1. Check changes to markdown (MD) with grip. `grip <file.md>`
    1. If it's not installed `pip3 install grip`
1. Do updates, edits, and code, test `flask run`
    1. if $FLASK_APP isn't set, `export FLASK_APP=<flask_app.py>`, first. Then `flask run`.
1. Switch back to master and merge new branch into master `git checkout master; git merge <new-branch-name>`
1. `git commit -a -m 'message'`
1. `git push origin master`

## Update production app
1. Easy way:
    `git push pythonanywhere`. This will push the master branch to the pythonanywhere bare repo and trigger a hook to build the app.
1. More comprehensive way:
    1. From pythonanywhere.com console run `git pull origin master`. That will replace the current running Flask app with the master branch's   head commit.
    1. Run `pip3 install -r requirements.txt`
        1. If the virtualenv is not activated, then you'll get permission errors. run `source bin/activate` to activate, and `deactivate` when/if done.
    1. Reload webapp from "pythonanywhere.com/user/jkmaxwell/webapps/#tab_id_www_pyhcalculator_com"
        1. Or from an ssh session run `reload_app.sh`. this just runs the `touch` command on "/var/www/www_pyhcalculator_com_wsgi.py"

## Tag and add release to master branch
1. If that worked created a tag/release and push it to origin.

How to get this running on a digitalocean droplet:
https://www.digitalocean.com/community/tutorials/how-to-structure-large-flask-applications
