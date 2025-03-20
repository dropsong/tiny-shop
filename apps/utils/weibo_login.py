import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.join(current_dir, '..', '..')
sys.path.append(project_dir)

from ShopProj.settings import AZURE_SERVER_IP


def get_auth_url():
    weibo_auth_url="https://api.weibo.com/oauth2/authorize"
    redirect_url="http://" + AZURE_SERVER_IP + ":8000/complete/weibo/"
    print(redirect_url)
    auth_url=weibo_auth_url+"?client_id={client_id}&redirect_uri={re_url}".format(client_id=4130988826,re_url=redirect_url)

    print(auth_url)


def get_access_token(code="2f0ee04f093085eb4a5337147bc4240b"):
    access_token_url="https://api.weibo.com/oauth2/access_token"
    import requests
    re_dict = requests.post(access_token_url,data={
        "client_id":1717642557,
        "client_secret":"1782eedd819f90e9455c1c97feec6e17",
        "grant_type":"authorization_code",
        "code":code,
        "redirect_uri":"http://149.129.53.199:8000/complete/weibo/"
    })
    pass


def get_user_info(access_token="",uid=""):
    user_url="https://api.weibo.com/2/users/show.json?access_token={token}&uid={uid}".format(token=access_token,uid=uid)
    print(user_url)


if __name__=="__main__":
    get_auth_url()
    # get_access_token(code="2f0ee04f093085eb4a5337147bc4240b")

    # get_user_info(access_token = "2.00VZhewGNSDPsB9fc4b102c80gjqoq",uid="6363525093")
