from flask import Flask,session
from flask_session import Session
import redis,os,sys
from dotenv import load_dotenv




def Create_App():
    app = Flask(__name__)
    
    
    env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.env_app"))
    load_dotenv(env_path)
    
    
    
    
    redis_host = os.getenv("REDIS_HOST", "redis-service")
    if ":" in redis_host:
        redis_host = redis_host.split(":")[0]  # Extract hostname only
        
        
    try:
        redis_client = redis.StrictRedis(host=redis_host, port=6379, db=0, decode_responses=True)
        redis_client.ping()
        print("✅ Successfully connected to Redis", flush=True)
    except redis.exceptions.ConnectionError:
        print("❌ Failed to connect to Redis", flush=True)
        sys.exit(1)  # Exit if Redis is not reachable

    app.secret_key = os.getenv('SECRET_KEY')
    # Configure Flask-Session
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_KEY_PREFIX'] = 'flask_session:'
    app.config['SESSION_REDIS'] = redis_host
        
    Session(app)

        
    
    
    
    #?app.config.from_object('config.Config') #!This line will import the Config class from the config.py file and load the configuration into the app object.
    
    #!When we use url_prefix, we are telling Flask to add the prefix to the URL of all the routes in the blueprint.
    from web.admin.routes import admin_bp #import the blueprint object 
    from web.Main_page.routes import Main_page_bp #import the blueprint object
    from web.login_page.routes import login_bp #import the blueprint object
    from web.api.routes import API_bp #import the blueprint object
    
    
    app.register_blueprint(admin_bp,url_prefix='/admin') #register the blueprint object in the app
    app.register_blueprint(Main_page_bp,url_prefix='/') #register the blueprint object in the app
    app.register_blueprint(login_bp,url_prefix='/login') #register the blueprint object in the app
    app.register_blueprint(API_bp,url_prefix='/api') #register the blueprint object in the app


    #Handle errors(404), if the page was not found
    @app.errorhandler(404)
    def not_found_error(error):
        return "This page was not found", 404
    
    return app







