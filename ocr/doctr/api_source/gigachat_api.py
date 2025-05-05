import typing
import os

from gigachat import GigaChat


class gigachat_api:
    def __init__(self):
        self.__giga__ = GigaChat(
            credentials=os.getenv('GIGACHAT_KEY'),
            verify_ssl_certs=False,
        )
        self.__prompt__ = os.getenv('PROMPT')

    def upload_file(self, file_with_text: typing.BinaryIO):
        self.__file_id__ = self.__giga__.upload_file(file_with_text).id_

    def delete_file(self):
        deleted_file_meta = self.__giga__.delete_file(self.__file_id__)
        if not deleted_file_meta.deleted:
            return False
        else:
            self.__file_id__ = None
            return True

    def request(self):
        if self.__file_id__ is None:
            return []
        else:
            return self.__giga__.chat(
                {
                    'messages': [
                        {
                            'role': 'user',
                            'content': self.__prompt__,
                            'attachments': [self.__file_id__],
                        }
                    ]
                })
