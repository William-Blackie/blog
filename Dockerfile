# Use 

FROM node:18 as frontend

COPY package.json package-lock.json postcss.config.js tailwind.config.js webpack.config.js ./
COPY ./website/static_src/ ./website/static_src/
COPY ./website/templates ./website/templates 

RUN npm ci && npm run build

# Use an official Python runtime based on Debian 10 "buster" as a parent image.
FROM python:3.8.1-buster as backend

# Add user that will be used in the container.
RUN useradd wagtail

# Port used by this container to serve HTTP.
EXPOSE 8000

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE"
#    command.
ENV PYTHONUNBUFFERED=1 \
    PORT=8000

# Install system packages required by Wagtail and Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadbclient-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
 && rm -rf /var/lib/apt/lists/*

# Configure Poetry
ENV POETRY_HOME="/opt/poetry" \
    POETRY_VERSION=1.2.0

# Add `poetry` to PATH
ENV PATH="$POETRY_HOME/bin:$PATH"

RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=${POETRY_VERSION} python3 - \
    && chmod 755 ${POETRY_HOME}/bin/poetry


# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Add bash commands
COPY scripts/bash.sh bash.sh

RUN touch /root/.bashrc \
 && cat bash.sh >> /root/.bashrc

# Install dependencies
COPY poetry.lock pyproject.toml ./

RUN /bin/true\
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction \
    && rm -rf /root/.cache/pypoetry

# Set this directory to be owned by the "wagtail" user. This Wagtail project
# uses SQLite, the folder needs to be owned by the user that
# will be writing to the database file.
RUN chown wagtail:wagtail /app

# Copy the source code of the project into the container.
COPY --chown=wagtail:wagtail . .
COPY --from=frontend ./website/static_compiled ./website/static_compiled

# Use user "wagtail" to run the build commands below and the server itself.
USER wagtail

# Collect static files.
RUN python manage.py collectstatic --noinput --clear

# Runtime command that executes when "docker run" is called, it does the
# following:
#   1. Migrate the database.
#   2. Start the application server.
# WARNING:
#   Migrating database at the same time as starting the server IS NOT THE BEST
#   PRACTICE. The database should be migrated manually or using the release
#   phase facilities of your hosting platform. This is used only so the
#   Wagtail instance can be started with a simple "docker run" command.
CMD set -xe; python manage.py migrate --noinput; gunicorn website.wsgi:application
