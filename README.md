这是一个工单系统，均通过Python进行编写，Python的版本为3.12.3.
本项目是开源项目，欢迎下载试用

如何生成语言包
python3 manage.py makemessages -l zh_Hans  # 或者 -l zh_CN，本代码表示生成简体中文语言包

如何编译语言包
python3 manage.py compilemessages  -i "venv"，其中，-i "venv"表示仅仅压缩本虚拟目录中

登陆授权Rest地址
http://localhost:8080/rest/auth/login?username=admin&password=admin&language=en
本代码中三个参数，分别表示用户名、密码与语言（英语），如果不指定返回语言，则采用中文

获取数据字典类型
http://localhost:8080/rest/system/dict-types/?format=json
如上链接返回json数据，实际使用时不需要/?format=json

正在进行自定义Rest异常