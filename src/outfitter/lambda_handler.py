from mangum import Mangum

from outfitter.server import app

handler = Mangum(app, lifespan="off")
