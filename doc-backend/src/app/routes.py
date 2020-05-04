import aiohttp_cors
from app.api import health, auth, profile, subscribe, news


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
    cors.add(app.router.add_put('/profile', profile.handler_update_profile))
    cors.add(app.router.add_get('/profile/{id_user}', profile.handler_get_profile))
    cors.add(app.router.add_get('/search/{search}', profile.search_profile_handler))
    cors.add(app.router.add_post('/subscribe', subscribe.subscribe_handler))
    cors.add(app.router.add_delete('/subscribe', subscribe.unsubscribe_handler))
    cors.add(app.router.add_post('/news', news.create_news_handler))
    cors.add(app.router.add_put('/news', news.update_news))
    cors.add(app.router.add_get('/news/{id_user}', news.get_news_by_handler))
    cors.add(app.router.add_get('/news_for_me/{id_user}', news.get_news_handler))
