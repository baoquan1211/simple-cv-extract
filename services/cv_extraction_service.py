import requests
from exceptions.exceptions import ServiceException


class ApiService:
    def __init__(self, url):
        self.api_url = url

    def request(self, content):
        pass


class CvExtractionService(ApiService):
    def __init__(self, url):
        super().__init__(url)

    def request(self, content: str):
        res = requests.post(url=self.api_url, data={"text": content})
        print(content)
        if res.status_code != requests.codes.ok:
            raise ServiceException("Service went wrong")
        result = res.json()
        return result["result"]["ents"]

    # def extract(self, content: str):
