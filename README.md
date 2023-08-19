# fastapi-llama2-chat-pdf

**Depreciated** Have a look at https://gitlab.com/pgryko/django-llama2-reactjs-chat-pdf for the django version.

A python LLM chat app backend using FastAPI and LLAMA2, that allows you to chat with multiple pdf documents.
Components are chosen so everything can be self-hosted.

Most useful trick in this repo is that we stream LLM output server side events (SSE) via StreamingResponse

Project using LLAMA2 hosted via replicate - however, you can self-host your own LLAMA2 instance.

This was originally being supposed to have a react frontend, but I ended up moving to async django
as it comes with user authentication and an orm out of the box.

Have a look at https://gitlab.com/pgryko/django-llama2-reactjs-chat-pdf for the django version.

## Getting started:

```shell
poetry install
poetry shell
uvicorn src.main:app --reload
```

```bash
$ poetry shell
$ python -m pytest
```

If you want pytest to fall into an ipython debugger shell on first failure

```bash
$ python -m pytest --pdbcls=IPython.core.debugger:Pdb -s
```

Auto Lint using https://github.com/psf/black, isort and flake8
```bash
$ black src
$ isort src --filter-files --profile black
$ flake8 --ignore=E501, W503, E722 --max-line-length=100 --max-complexity=10 src/
```

## Testing gitlab pipeline on localmachine

It's possible to install gitlab runner on your local machine and test the .gitlab-ci.yaml

```bash
$ gitlab-runner exec docker test\ python
```




## License
MIT
