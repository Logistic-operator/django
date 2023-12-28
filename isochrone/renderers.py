import json

from rest_framework.renderers import JSONRenderer


class IsochroneJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        status_code = data.get('detail', None)

        if not status_code:
            return json.dumps({
                'isochrone': data
            })
        
        return super(IsochroneJSONRenderer, self).render(data)