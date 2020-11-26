# [sso 单点登录](https://github.com/chaleaoch/gitblog/issues/26)


Table of Contents
=================



\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*
多个子系统拥有同一个认证系统.
实现在任意一个子系统登陆之后,所有系统都可以进行资源访问.
也可以提供统一的注册接口,登陆页面等.
认证系统的主要功能是认证, 用户信息可以保存在认证系统中,也可以保存在子系统中. 
这是客户端的例子
https://github.com/chaleaoch/django_sso_client_2/tree/master
这是服务端的例子.
https://github.com/chaleaoch/django-sso