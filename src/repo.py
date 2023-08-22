class Repository:
    def __init__(self, uid: str, clone_url: str, name: str, path: str) -> None:
        self.uid = uid
        self.clone_url = clone_url
        self.name = name
        self.path = path