# 简单密码管理器应用的实现
首先，你需要安装 cryptography 库，用于实现AES加密。  
pip install cryptography
## 代码说明：
**PasswordManager 类**：处理密码管理的核心类。

- generate_key：使用主密码和盐生成AES加密密钥。
- encrypt_password：使用AES-GCM模式加密密码。
- decrypt_password：解密存储的密码。
- store_password：将加密后的密码存储在JSON文件中。
- retrieve_password：从存储中检索并解密密码。
- generate_strong_password：生成一个随机的强密码，包含大小写字母、数字和特殊字符。

**密码加密**：使用AES-GCM算法确保密码存储的安全性，AESGCM是高度安全的认证加密模式。

**主密码**：主密码是用于生成加密密钥的核心，这个密码必须被妥善保护。

**密码存储**：使用JSON文件存储账户名与对应的加密密码，确保密码不会明文保存。

**使用方法**：
输入你的主密码，这个密码将用于加密和解密你的账户密码。
输入账户名称，生成强密码并将其加密存储。
输入账户名称来检索密码，系统会自动解密并展示明文密码。
