# med_backend
## Poetry

API docs - https://dev2.akarpov.ru/api/docs

This project uses poetry. It's a modern dependency management
tool.

To run the project use this set of commands:

```bash
poetry install
poetry shell
python3 -m med_backend
```

## Docker

You can start the project with docker using this command:

```bash
docker-compose -f deploy/docker-compose.yml --project-directory . up --build
```

## Configuration

This application can be configured with environment variables.

You can create `.env` file in the root directory and place all
environment variables here.

All environment variabels should start with "MED_BACKEND_" prefix.

For example if you see in your "med_backend/settings.py" a variable named like
`random_parameter`, you should provide the "MED_BACKEND_RANDOM_PARAMETER"
variable to configure the value. This behaviour can be changed by overriding `env_prefix` property
in `med_backend.settings.Settings.Config`.

An exmaple of .env file:
```bash
MED_BACKEND_RELOAD="True"
MED_BACKEND_PORT="8000"
MED_BACKEND_ENVIRONMENT="dev"
```

## Pre-commit

To install pre-commit simply run inside the shell:
```bash
pre-commit install
```

pre-commit is very useful to check your code before publishing it.
It's configured using .pre-commit-config.yaml file.

By default it runs:
* black (formats your code);
* mypy (validates types);
* isort (sorts imports in all files);
* flake8 (spots possibe bugs);
* yesqa (removes useless `# noqa` comments).
