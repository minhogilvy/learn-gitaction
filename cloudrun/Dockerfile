FROM --platform=linux/amd64 python:3.8-slim-bookworm as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"
######################################################
# DEVELOPMENT STAGE
######################################################
ENV HOST 0.0.0.0
ENV PORT 8000
FROM python-base as development

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . /app

WORKDIR /app
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 8 --timeout 0 --worker-class uvicorn.workers.UvicornWorker app.main:app