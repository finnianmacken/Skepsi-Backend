# How to do everything interesting

## ...after cloning
This will install the packages the frontend needs.
```
cd skepsi_frontend
yarn install
```

## to run storybook
```
cd skepsi_frontend
yarn storybook
```

## to run the frontend server
Hint: this is not what you want. Run storybook instead.
```
cd skepsi_frontend
yarn start
```

## to run the backend server

```
cd skepsi_backend
python3 manage.py runserver
```
The GraphiQL interface is on the default server endpoint



# Production Documentation

Push a new build of master to heroku with:
```
git push heroku master
```
You must be in the appropriate git repository to do so

Production and development settings should be configured using the .env files in backend and frontend. Comment out all variables (#) that are associated with production/development, and uncomment those associated with development/production


Every time you add a new library to the backend, you need to:
- install it with poetry: poetry add <foo>
- freeze poetry into a new requirements.txt file:
```
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

If you try to push to heroku, and you get an error message about concurrent builds, try (in order):
```
heroku builds:cancel

heroku builds:cache:purge

heroku restart

*wait a bit*

git push heroku master

```

If this doesn't work, find Finn.

Production servers remain running with their git version until they're updated with git push. This means that you will still be able to access the (old) production build while working with the development build. Make sure if you're adding something to the production build that you set all of the variables correctly.
