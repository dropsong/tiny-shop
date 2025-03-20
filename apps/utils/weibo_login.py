import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.join(current_dir, '..', '..')
sys.path.append(project_dir)

from ShopProj.settings import AZURE_SERVER_IP


def get_auth_url():
    weibo_auth_url="https://api.weibo.com/oauth2/authorize"
    # redirect_url="http://" + AZURE_SERVER_IP + ":8000/complete/weibo/"
    redirect_url="http://127.0.0.1:8000/complete/weibo/"
    print(redirect_url)
    auth_url=weibo_auth_url+"?client_id={client_id}&redirect_uri={re_url}".format(client_id=4和谐6,re_url=redirect_url)

    print(auth_url)


def get_access_token(code="和谐"):
    access_token_url="https://api.weibo.com/oauth2/access_token"
    import requests
    response = requests.post(access_token_url,data={
        "client_id":4和谐6,
        "client_secret":"5和谐c",
        "grant_type":"authorization_code",
        "code":code,
        "redirect_uri":"http://127.0.0.1:8000/complete/weibo/"
    })
    re_dict = response.json()
    print(re_dict)
    # {'access_token': '2和谐V', 'remind_in': '157679999', 'expires_in': 157679999, 'uid': '和谐', 'isRealName': 'true'}


def get_user_info(access_token="2和谐V",uid="7和谐8"):
    user_url="https://api.weibo.com/2/users/show.json?access_token={token}&uid={uid}".format(token=access_token,uid=uid)
    print(user_url)


if __name__=="__main__":
    # get_auth_url()
    # get_access_token()

    get_user_info()
