import json
from django.http import HttpResponse


def status(request):
    payload = {
        "status": "UP"
    }
    return HttpResponse(json.dumps(payload), content_type="application/json")
