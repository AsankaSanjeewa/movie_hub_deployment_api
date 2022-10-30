#!/usr/env/bin sh
# start

set -o errexit
set -o pipefail
set -o nounset

python /app/manage.py collectstatic --noinput
python /app/manage.py migrate   # WARNING: Not a good idea for prod
gunicorn core.wsgi:application --bind 0.0.0.0:5000 --chdir=/app
celery -A core worker -l info


