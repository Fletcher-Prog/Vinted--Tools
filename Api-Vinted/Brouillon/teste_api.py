from flask import Flask

# For start project flask --app name_file_project run


app = Flask(__name__)

@app.route('/{name}')
def vinted_link():
    return name