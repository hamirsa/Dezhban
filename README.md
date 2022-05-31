# Dezh-Ban

Dezh-Ban helps you with user sign up/in using using OTP


## Technologies used

* [Python 3.9](https://www.python.org) , Programming Language.
* [Django 4.0](https://docs.djangoproject.com/en/4.0/) , Web Framework.
* [Django Rest Framework 3.13](https://www.django-rest-framework.org/) , Web API's.
* [Docker](https://docker.com/) , Container Platform.
* [Git](https://git-scm.com/doc) , Version Control System.
* [Celey](https://docs.celeryq.dev/en/stable/) , Distributed Task Queue
* [Redis](https://redis.io/docs/) , Cache Database and message broker
* [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) , Authentication Manager


## Requirements

* **install [Docker](https://www.docker.com/)**  
You must install Docker to run **Redis** container on it.
  * [install Docker on Linux](https://docs.docker.com/engine/install/)
  * [install Docker on Windows](https://docs.docker.com/desktop/windows/install/)
  * [install Docker on Mac](https://docs.docker.com/desktop/mac/install/)

* **install [Postman](https://www.postman.com/)(recommended) _or_ [Thunder Client](https://www.thunderclient.com)**  
To test api, you need to use postman app **or** thunder client extension on vscode  

  Postman  
  * [install postman on Linux](https://learning.postman.com/docs/getting-started/installation-and-updates/#installing-postman-on-linux)
  * [install postman on Windows](https://learning.postman.com/docs/getting-started/installation-and-updates/#installing-postman-on-windows)
  * [install postman on Mac](https://learning.postman.com/docs/getting-started/installation-and-updates/#installing-postman-on-mac)

  > use this [Guide](https://learning.postman.com/docs/sending-requests/requests/) on how to send request via **postman**. 

  Thunder Client(**note**: you won't need this, if you've installed Postman)  
       
  Launch VS Code Extensions tab (Ctrl+Shift+X), search for _Thunder Client_ and install it.

  > use this [Guide](https://developers.refinitiv.com/en/article-catalog/article/how-to-test-http-rest-api-easily-with-visual-studio-code---thund) on how to send request via **thunder client**.


## Installation

1. **clone the project**  
   ```  
   git clone git@github.com:hamirsa/Dezhban.git 
   ```  

2. **move '.env-sample' to the path dezhban/dezhban/, rename it to '.env', and provide required variables**.  
   ```
   mv .env-sample dezhpad/.env  
   ```
   Pay attention that in this project we're using [SMS.IR](https://sms.ir/) APIs to send OTP.  
   **note**: you will need an API_KEY which is accessible in your dashboard.

3. **create a python virtual environment**  
   ```
   python -m venv venv
   ```

4. **activate your venv**
  * on linux and mac
    ```
    source venv/bin/activate
    ```
  * on windows
    ```
    venv/Scripts/activate
    ```

5. **install dependencies**
   ```
   pip install -r requirements.txt
   ```

6. **run a redis container on docker**
   ```
   docker network create redisnet
   docker run -d -p 6379:6379 --name cache-redis --network redisnet redis
   ```

7. **run a celery worker in a seprated terminal tab**
   ```
   celery -b redis://localhost:6379 -A api.tasks worker -E -Q otp --loglevel INFO
   ```

8. **migrate**
   ```
   python manage.py migrate
   ```

9. **run project**
   ```
   python manage.py runserver
   ```

## Testing Dezh-Ban APIs

The login senario would be like this:  
1. Client's phone number would be sent by a post request to 'send-otp' endpoint. Then user will receive an sms containing OTP code.
2. Client's phone number and delivered OTP code must be sent by a Post request to 'verify-otp' endpoint. If client provides the correct information, it's request would be Responsed by an access and refresh token for further usages(authentication).

**send-otp**
send a post request to (https://localhost:8000/api/send-otp/) including "phone_number" in it's body.  
you will receive an sms containig OTP code asap.(you would see it in the celery logs if you are not using an SMS provider as explained in step2.)

**verify-otp**  
send a post request to (https://localhost:8000/api/verify-otp/) including "phone_number" and "otp" in it's body.  
you will Responded by an access and refresh token if you provide correct information.

**check your token**
send a get request to (https://localhost:8000/api/home) including access token in Headers like below:  
```
# key: Authorization
# value: Bearer your-token-without-quotation-marks
```  

if you provide correct credentials you will receive this Response:  
```
{
    "detail": "you can see this, so you've done great so far :)"
}
```