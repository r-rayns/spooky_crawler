import json
from spooky_crawler.utils import Dictionary


class Extractor():
    def __init__(self):
        pass

    def extract(self, document, selectors, *json_property):
        # see if the document has any json linked data
        json_linked_data = document.xpath(
            '//script[@type="application/ld+json"]//text()').getall()

        if json_linked_data:
            # try to extract json property, fallback to selector if not
            return self._processJson(json_linked_data, *json_property) or self._try_selectors(document, selectors)
        else:
            return self._try_selectors(document, selectors)

    def _processJson(self, json_array, *json_property):
        for json_data in json_array:
            parsed_json = json.loads(json_data)
            json_value = Dictionary(parsed_json)\
                .safeGet(*json_property)\
                .value
            if json_value:
                return  json_value

    # recursivly run selector functions against the document until a value is found
    # or we run out of selectors
    def _try_selectors(self, document, selectors):
        value = selectors[0](document)
        if (value == None or value == '') and len(selectors) > 1:
            value = self._try_selectors(document, selectors[1:])

        return value
