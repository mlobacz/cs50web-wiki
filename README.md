# Wiki

HarvardX's Computer Science for Web Programming project 1 submission.

## Objective

Design a Wikipedia-like online encyclopedia.
[Full task description](https://cs50.harvard.edu/web/2020/projects/1/wiki/).

## Demo video

[Demonstration video](https://youtu.be/ANBIkapFCRw).

## Running locally

1. Clone this git repository

    ```bash
    git clone https://github.com/mlobacz/cs50web-wiki.git
    ```

2. Change into projects root directory.

    ```bash
    cd cs50web-wiki
    ```

3. Create and activate new virtual environment

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

4. Install pip-tools

    ```bash
    pip install pip-tools
    ```

5. Install python requirements

    ```bash
    pip-sync requirements.txt dev-requirements.txt
    ```

6. Apply migrations to your database

    ```bash
    python manage.py migrate
    ```

7. Run unit tests

    ```bash
    python manage.py test
    ```

8. Run app locally

    ```bash
    python manage.py runserver
    ```
