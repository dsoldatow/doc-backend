import aiohttp_cors
from app.api import health, auth


def setup_routes(app):
    cors = aiohttp_cors.setup(app, defaults={
        '*': aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers='*',
            allow_headers='*',
        ),
    })
    cors.add(app.router.add_get('/healthz', health.health_check))
    cors.add(app.router.add_post('/auth/sign_in', auth.auth_handler))
    cors.add(app.router.add_post('/auth/sign_up', auth.sign_up_handler))
