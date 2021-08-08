from html.parser import HTMLParser

class SmiteHtmlObject:
    def __init__(self):
        self.description = ""
        self.map_data = ""
        self.additional_data = []

class SmiteHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.smite_object = SmiteHtmlObject()
        self.data_count = 0
        self.information = []

    def handle_starttag(self, tag, attrs):
        try:
            self.information.append(tag)
        except Exception as e:
            print(e)

    def handle_endtag(self, tag):
        try:
            self.information.append(tag)
        except Exception as e:
            print(e)

    def handle_data(self, data):
        try:
            if self.data_count == 0:
                self.smite_object.description = data
            elif any(item in str(data).lower() for item in ["arena", "conquest", "assault"]):
                self.smite_object.map_data = str(data).lower().replace('map:', '').strip().capitalize()
            else:
                self.smite_object.additional_data.append(data)
            self.data_count += 1

        except Exception as e:
            print(e)