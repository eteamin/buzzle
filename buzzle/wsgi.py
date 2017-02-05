from aiohttp.web import Application, run_app

from buzzle.controllers import post


app = Application()
app.router.add_post('/apiv1/', post)
# buzzle_app.router.add_get('/apiv1/', get)

run_app(app)
