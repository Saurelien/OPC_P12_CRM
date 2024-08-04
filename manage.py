from collaborator_app.controller import MainController
from initiate_database import create_database
import sentry_sdk
from config import config

sentry_sdk.init(
    dsn="https://5251857df045ea49f3def4f1cd90851f@o4506552407097344.ingest.us.sentry.io/4507268735303680",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

config.TEST = False
create_database()
MainController.run()
