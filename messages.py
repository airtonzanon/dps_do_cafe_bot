import os.path
import json


class Message:

    def __init__(self, document_name: str):
        self.document_name = document_name
        self.document_content = self.read_file()

    def read_file(self):
        if os.path.exists(self.document_name):
            document = open(self.document_name, 'rb')
            document_content = document.read().decode()
            if document_content:
                return json.loads(document_content)

        return {}

    def write_on_file(self, new_data):
        document = open(self.document_name, 'w+')

        old_data = self.document_content
        data = {**old_data, **new_data}

        document.write(json.dumps(data))

    def re_write(self, key, text):
        document = open(self.document_name, 'w+')

        self.document_content[key] = [text]

        document.write(json.dumps(self.document_content))

    def verify_exists(self, key, text):
        try:
            channel_member = self.document_content[key]

            return text in channel_member
        except KeyError:
            return False

    def add_message(self, key, text):
        try:
            channel_member = self.document_content[key]

            channel_member.append(text)
        except KeyError:
            self.document_content.update({
                key: [text]
            })

        self.write_on_file(new_data=self.document_content)
