from app import app

if __name__ == "__main__":
	app.run()

# to run -> gunicorn --bind 0.0.0.0:7766 wsgi:app -D