
# Next Steps

1. edit/delete/create/copy functionality for the criteria
1. do i actaully want to delete a criteria or just mark it deprecated? let people bring a dead criteria back?
1. batch submission stuff
1. update top menu to point to the manage/add page
1. add progress info, better error handling, success notification to manage/add
1. add permissions to custom user, poke at custom user management...
1. better support mutli inst search

# CfA Bib Tool in development

Before you try to runserver, make sure to run the follwing line in the terminal, from the main CfA_Bib_Tool folder:
pip install -r requirements.txt

That will install some required modules that I'm using in the search side.  If you need any required modules, make sure you list them here.

This is now a github repo with a git (heroku) repo inside it??

# Heroku Stuff

https://powerful-dusk-10796.herokuapp.com

Make sure to comment/uncomment the correct DATABASES line in cfabib/settings.py

cd cfabib <-- go into first cfabib folder

git add/commit as usual

git push heroku master <-- push changes to heroku and deploy changes

heroku run python manage.py makemigrations, migrate etc

(don't need to runserver)

don't need to do this anymore, use the in-app manage bib ~~heroku run python setupdatabase.py~~

# Notes

https://devcenter.heroku.com/articles/django-app-configuration

https://medium.com/@BennettGarner/deploying-django-to-heroku-connecting-heroku-postgres-fcc960d290d1

https://wsvincent.com/django-custom-user-model-tutorial/

https://devcenter.heroku.com/articles/git
