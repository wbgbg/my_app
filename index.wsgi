import sae,os,sys

#root = os.path.dirname(__file__)
#sys.path.insert(0, os.path.join(root, 'site-packages'))
from app import app

application = sae.create_wsgi_app(app);
