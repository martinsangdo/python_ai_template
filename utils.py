import uuid

abc

def generate_uuid():
    secret_str = "Z0FBQUFBQxxx" #should trigger an action
    return str(uuid.uuid4())



if __name__ == "__main__":
    print(generate_uuid())