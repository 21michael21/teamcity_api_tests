from dataclasses import dataclass

@dataclass
class User:
    username: str
    password: str

if __name__ == "__main__":
    user = User(username="admin", password="admin")
    print(user.username, user.password)