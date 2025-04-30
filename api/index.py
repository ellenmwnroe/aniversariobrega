from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "App Flask no Vercel!"

# Export para o Vercel
def handler(request):
    return app(request)