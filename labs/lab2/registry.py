class Race:
    """
    Attributes: Name, Email, Speed Category
    Methods: getRunners, RunnerCategory, changeEmail, changeCategory, Withdraw
    """
    name: str
    email: str
    speedCat: str

    def __init__(self, name: str, email: str, speedCat: str):

        self.name = name
        self.email = email
        self.speedCat = speedCat

    def getRunners(self, ctgry:str) -> list[]:


