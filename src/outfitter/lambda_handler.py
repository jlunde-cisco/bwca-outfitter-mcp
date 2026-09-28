from mangum import Mangum

from outfitter.server import create_app


def handler(event, context):
    return Mangum(create_app(), lifespan="auto")(event, context)
