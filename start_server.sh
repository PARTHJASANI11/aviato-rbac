# Start the gunicorn server

echo "Starting gunicorn server..."
gunicorn -k uvicorn.workers.UvicornWorker -b 0.0.0.0:5000 app.main:app