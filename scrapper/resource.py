from django.conf import settings
import requests


class DHISAPI:
    def __init__(self) -> None:
        self.store = []
        self.url = settings.CARPHA_API_URL
        self.username = settings.CARPHA_API_USERNAME
        self.password = settings.CARPHA_API_PASSWORD
        
    def reset_store(self):
        self.store = []
        
    def make_url(self, path:str, **kwargs):
        url = f"{self.url}/{path}"

        if kwargs:
            url += "?"
            if "pageSize" not in kwargs:
                url += "paging=false&"
            for k, v in kwargs.items():
                url += f"{k}={v}&"
            url = url[:-1]            
        return url
        
    def fetch(self, url: str, reset_store: bool=True) -> list[dict]:
        if reset_store:
            self.reset_store()
        
        response = requests.get(url, auth=(self.username,self.password))
            
        data = response.json()
        self.store.append(data)
        
        # recurse through
        pager = data.get("pager", None)
        if pager:
            next_page = pager.get("nextPage", None)
            if next_page:
                self.fetch(next_page, False)
        return self.store
    
    def send(self, url: str, data=None):
        response = requests.post(url, json=data, auth=(self.username,self.password))
        if response.status_code != 200:
            print("failed to post data")
            print(response.status_code)
            print(response.reason)
            return
        
        return response.json()
