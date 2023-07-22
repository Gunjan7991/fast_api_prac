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


## To run the app using Docker:
    First,  to refresh the docker image, for if any changes are made,  we need to run: "docker build -t fastapi ."  

    where, 
            docker build  --> is the base command.
            -t "Name"    --> GIVES  name to the image
            .           --> means inside the current folder (we need to give it a path)


