import uuid

def generate_uuid():
    secret_str = "aaa" #should trigger an action
    return str(uuid.uuid4())



if __name__ == "__main__":
    print(generate_uuid())