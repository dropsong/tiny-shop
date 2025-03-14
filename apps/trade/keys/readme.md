
这个文件夹应当存放公钥 pub_2048、私钥 ``private_2048.txt``、由支付宝加签后的公钥 ``alipay_key_2048``，由 gitignore 隐去了。

![pic1](./1.png)

![pic2](./2.png)

**注意**：RSA2 加密算法默认生成格式为 PKCS8（Java适用），如需 PKCS1 格式（非Java适用），需要格式转换。
