<p align="center">
<img src ="assets/ufc.svg" width=400px>
</p>

# About

This is a project that idealizes an open api from University Federal of Ceará (UFC) at Quixadá's campus (https://www.quixada.ufc.br/). 

Api provides some info such as: disciplines, teachers and subjects. 

# Documentation

There are only 3 main endpoints, all of them are **GET**.

## Get all disciplines (/disciplines) GET

```json
[
    {
        "id": "QXD0157",
        "name": "Trabalho de Conclusão de Curso I",
        "hours": "32",
        "pre_requisite": null,
        "courses": [
            "CC"
        ]
    },
    {
        "id": "QXD0012",
        "name": "Probabilidade e Estatística",
        "hours": "64",
        "pre_requisite": "QXD0056",
        "courses": [
            "CC"
        ]
    }
]

```

## Get all teacher (/teacher) GET

 ```json
 [
    
    {
        "id": "ANLISA",
        "name": "Andréia Libório Sampaio",
        "disciplines": [
            "QXD0024",
            "QXD0049",
            "QXD0189",
            "QXD0027",
            "QXD0038"
        ]
    },
    {
        "id": "LUISBEFR",
        "name": "Lucas Ismaily Bezerra Freitas",
        "disciplines": [
            "QXD0017",
            "QXD0016",
            "QXD0008",
            "QXD0025",
            "QXD0152"
        ]
    }
 ]
 ```

 ## Get all subjects (/subject) GET

 ```json
 [

    {
        "discipline": {
            "id": "QXD0016",
            "name": "Linguagens de Programação",
            "hours": "64",
            "pre_requisite": "QXD0007",
            "courses": [
                "CC"
            ]
        },
        "teacher": {
            "id": "CRPESO",
            "name": "Criston Pereira de Souza",
            "disciplines": [
                "QXD0016",
                "QXD0008",
                "QXD0182",
                "QXD0010",
                "QXD0001",
                "QXD0012",
                "QXD0056",
                "QXD0041"
            ]
        },
        "id": "QXD0016-CRPESO"
    },
    {
        "discipline": {
            "id": "QXD0116",
            "name": "Álgebra Linear",
            "hours": "64",
            "pre_requisite": null,
            "courses": [
                "CC"
            ]
        },
        "teacher": {
            "id": "ANRIBR",
            "name": "André Ribeiro Braga",
            "disciplines": [
                "QXD0214",
                "QXD0109",
                "QXD0218",
                "QXD0144",
                "QXD0013",
                "QXD0148",
                "QXD0145",
                "QXD0012",
                "QXD0005",
                "QXD0116",
                "QXD0001",
                "QXD0147",
                "QXD0006"
            ]
        },
        "id": "QXD0116-ANRIBR"
    }
 ]
 ```

#### Just a note

All of these 3 routes has a equivalent one if you wanna get some entity by id Example: /disciplines -> disciplines/QXD0007 will return:

```json
{
    "id": "QXD0007",
    "name": "Programação Orientada a Objetos",
    "hours": "64",
    "pre_requisite": "QXD0001",
    "courses": [
        "CC"
    ]
}
```

And the same goes for the others: ***/subject*** and ***/teacher***

# How to run?

First, create `.env` like this:

```
API_HOST=localhost
API_PORT=8888
APP_PROFILE=LOCAL
REDIS_PORT=6379
REDIS_HOST=localhost
```
And then: 

If you have **Docker Compose** installed on your machine, just run:

```
docker compose up
```

If you **don't** have installed or you just wants to run locally without docker, you have to make some changes: 

- On the file `scrapping/try_connection.py` paste the following code:

```python    
def try_connection():
    print("Trying to connect to selenium server...") 
    opts = webdriver.FirefoxOptions()
    opts.add_argument('--no-sandbox')
    opts.add_argument('--headless')
    opts.add_argument('--disable-popup-blocking')

    return webdriver.Firefox(
        options=opts
    )
```

> If you don't have Firefox Installed or wants to use another browser, search on Selenium docs to adapt this code to your scenario

- Install dependencies
```
pip install --no-cache-dir -r requirements.txt
```
- Run the application
```
python3 main.py
```
# How to contribute?

If you somehow wants to contribute with this project, I have planned and map some ideas: 

- Just provide feedback, it'll be useful
- How to get the actual semester of a discipline? 
- How to map and save disciplines from another courses? Right now i'm only providing Computer Science course. 
- How to deploy this API freely?
- How to be more generic and implement this for all UFC's campus? 
- Is there a way to do this more fancy? Without webscrapping?
    - Is there a way to improve the webscrapping?


# Contact 

You can find me on my linkedin: https://www.linkedin.com/in/ren%C3%AA-j%C3%BAnior-55901b198/