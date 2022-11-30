if [ -z "${PORT}" ]
then
  PORT=8080
fi

if [ -z "${VENV_PATH}" ]
then
  VENV_PATH='.venv'
fi

if [ -d "$VENV_PATH" ]
then
    source .venv/bin/activate
else
    echo "Create virtual environment with name=.venv or set existing path to VENV_PATH virtual environment variable"
    exit 0
fi

echo "Starting service on port $PORT"
echo "To change port set port to PORT virtual environment variable"
gunicorn -b :$PORT core.wsgi:application
