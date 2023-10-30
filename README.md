# worldfy 

## Setting up development enviroment
### Setting up PostgreSQL database
* Open terminal or WSL terminal if you are working on Windows.
* Update Ubuntu packages:
    ```sudo apt update```

* Install PostgreSQL 
    ```sudo apt install postgresql postgresql-contrib```
    Confirm installation and get version number: ```psql --version```

* Set a password to defaulf admin user 
    ```sudo passwd postgres```

* Access psql using ```sudo -u postgres psql```

* List databases ```\l```

* Connect to database ```\c [database_name]```
### Setting up backend packages
* Open terminal or WSL terminal if you are working on Windows.
* Install the packages according to the configuration file:
    ```pip install -r requirements.txt```
* If during work you needed to install new packages, overwrite requirements.txt file using:
    ```pip freeze > requirements.txt```