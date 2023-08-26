# fast_api_prac

## Python Version: 3.9.6+

## To run the app manually:

    -   For best practice, use virtual env.
            python3 -m venv venv

    -   If virtual env is used, activate the virtual env.
            source venv/bin/activate [mac os / linux]
            . venv/bin/activate      [windows]

    -   First we need to download all the dependencies for the project by running pip command.
            pip install -r requirements.txt

    -   uvicorn app.main:app "--host []" "--port []" :=> where " "-> means optional parameters.
            uvicorn app.main:app

    default for fastapi is:

        uvicorn main:app

        we are using "app.main:app" --> because of our folder structure. Since we got our main.py file inside of app folder.

        "--reload"  only use in Non_Prod. Used in non_prod becasue it restarts the server afther the code change.

        "--host" run the server in the particular hostname, e.g 0.0.0.0 or 127.0.0.1. on default, runs on localhost/127.0.0.1

        "--port" specifies the port number in which the server will server the application. on default runs on port 8000

## Docker


### Building Container

After making all the changes you want in docker-compose.yml file, run:

```
docker-compose build or docker-compose -f docker-compose-[dev/prod].yml build
```

Let it download all the dependencies for FastApi app. Once this command runs successfully, run:

```
docker-compose up -d or docker-compose -f docker-compose-[dev/prod].yml up -d
```

### HTTPS API

Install mkcert in you server by running:
```
apt install mkcert
```

Then, You need to generate the certificate and add to your CA with the mkcert utility:
```
mkcert -install
mkcert app.example.com localhost 127.0.0.1 ::1
```

substitue app.example.com with you " " if you don't have any website or with "name of your website" if you have one

add following when you run uvicorn:

```
uvicorn app.main:app --host 0.0.0.0 --port 8000 --ssl-keyfile your_key.pem --ssl-certfile your_cer.pem
```
