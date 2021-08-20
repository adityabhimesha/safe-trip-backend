import kronos
from .models import Tokens


@kronos.register('0 */12 * * *')
def resetTrending():
    # your functionality goes here
    trending = Tokens.objects.filter(is_trending=True)
    for token in trending:
        token.is_trending = False
        token.views = 0
        token.save()
