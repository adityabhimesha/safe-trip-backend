import kronos
from .models import Tokens


@kronos.register('* * * * *')
def my_cron_job():
    # your functionality goes here
    trending = Tokens.objects.filter(is_trending=True)
    for token in trending:
        token.is_trending = False
        token.save()

    