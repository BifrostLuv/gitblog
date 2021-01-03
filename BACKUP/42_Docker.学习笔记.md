# [Docker 学习笔记](https://github.com/chaleaoch/gitblog/issues/42)


Table of Contents
=================

   * [概述](#概述)
      * [docker 配置](#docker-配置)
      * [镜像管理](#镜像管理)
   * [Dockerfile](#dockerfile)
      * [USER/WORKDIR](#userworkdir)
      * [ADD/EXPOSE](#addexpose)
      * [RUN/ENV](#runenv)
      * [CMD/ENTRYPOINT](#cmdentrypoint)
      * [CMD](#cmd)
      * [ENTRYPOINT](#entrypoint)
   * [网络模型](#网络模型)

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*
# 概述

容器技术依赖内核虚拟化技术(LXC)实现

- namespaces

![](https://tcs.teambition.net/storage/3121dc317ce0e40fbd31946a63b48d0a9be0?Signature=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJBcHBJRCI6IjU5Mzc3MGZmODM5NjMyMDAyZTAzNThmMSIsIl9hcHBJZCI6IjU5Mzc3MGZmODM5NjMyMDAyZTAzNThmMSIsIl9vcmdhbml6YXRpb25JZCI6IiIsImV4cCI6MTYxMDI3OTk2MCwiaWF0IjoxNjA5Njc1MTYwLCJyZXNvdXJjZSI6Ii9zdG9yYWdlLzMxMjFkYzMxN2NlMGU0MGZiZDMxOTQ2YTYzYjQ4ZDBhOWJlMCJ9.YzrfZs5kkoph2cT6u7LozZMJsAXq-tMqwQkGeEUv14Q&download=image.png "")

- cgroups -- cpu 内存等资源的控制

和其他虚拟化技术相比, 减少了guest os 这一层封装.效率更高.

![](https://tcs.teambition.net/storage/3121e35fa6fee5ca90213c86c91dd18f5ed8?Signature=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJBcHBJRCI6IjU5Mzc3MGZmODM5NjMyMDAyZTAzNThmMSIsIl9hcHBJZCI6IjU5Mzc3MGZmODM5NjMyMDAyZTAzNThmMSIsIl9vcmdhbml6YXRpb25JZCI6IiIsImV4cCI6MTYxMDI3OTk2MCwiaWF0IjoxNjA5Njc1MTYwLCJyZXNvdXJjZSI6Ii9zdG9yYWdlLzMxMjFlMzVmYTZmZWU1Y2E5MDIxM2M4NmM5MWRkMThmNWVkOCJ9.mz6oamILxQI5O8OoMp71UsBZfCyOr_um2m1_bvtbhaM&download=image.png "")

## docker 配置

```shell
[root@node4 docker]# cat /etc/docker/daemon.json 
{
  "graph": "/data/docker",     # docker工作目录
  "storage-driver": "overlay2",   # 存储驱动
  "insecure-registries": ["registry.access.redhat.com","quay.io"],  # 不安全的仓库
  "registry-mirrors": ["https://q2gr04ke.mirror.aliyuncs.com"],  # 加速镜像
  "bip": "172.6.244.1/24",   # docker的网络,尽量要与宿主机有个对照关系
  "exec-opts": ["native.cgroupdriver=systemd"],  # cgroup的类型
  "live-restore": true  # 让docker容器不依懒docker引擎的死与活
}
```

## 镜像管理

1. 登录

```shell
[root@node4 ~]# docker login docker.io
Login with your Docker ID to push and pull images from Docker Hub. If you don't have a Docker ID, head over to https://hub.docker.com to create one.
Username: sunrisenan
Password: 
WARNING! Your password will be stored unencrypted in /root/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded

[root@node4 ~]# cat /root/.docker/config.json 
{
    "auths": {
        "https://index.docker.io/v1/": {
            "auth": "c3VucmlzZW5hbjpseXo1MjAx="
        }
    },
    "HttpHeaders": {
        "User-Agent": "Docker-Client/19.03.4 (linux)"
    }
}[root@node4 ~]# echo "c3VucmlzZW5hbjpseXo1MjAx="|base64 -d
sunrisenan:123

```

1. 打tag

```text
[root@node4 ~]# docker tag 965ea09ff2eb docker.io/sunrisenan/alpine:3.10.3
```

1. 推送

```text
[root@node4 ~]# docker push docker.io/sunrisenan/alpine:3.10.3
The push refers to repository [docker.io/sunrisenan/alpine]
77cae8ab23bf: Mounted from library/alpine 
3.10.3: digest: sha256:e4355b66995c96b4b468159fc5c7e3540fcef961189ca13fee877798649f531a size: 528

```

1. 删除镜像标签及镜像

```text
[root@node4 ~]# docker rmi -f 965ea09ff2eb   # -f 强制删除（包括标签及镜像）
Untagged: alpine:latest
Untagged: alpine@sha256:c19173c5ada610a5989151111163d28a67368362762534d8a8121ce95cf2bd5a
Untagged: sunrisenan/alpine:3.10.3
Untagged: sunrisenan/alpine@sha256:e4355b66995c96b4b468159fc5c7e3540fcef961189ca13fee877798649f531a
Deleted: sha256:965ea09ff2ebd2b9eeec88cd822ce156f6674c7e99be082c7efac3c62f3ff652
Deleted: sha256:77cae8ab23bf486355d1b3191259705374f4a11d483b24964d2f729dd8c076a0
```

# Dockerfile

## USER/WORKDIR

```yaml
FROM sunrisenan/nginx:v1.12.2
USER nginx
 # PID 1号进程是用什么用户运行的.
WORKDIR /usr/share/nginx/html # CD类似

```

## ADD/EXPOSE

- ADD比COPY多一些额外的功能, 譬如 可以复制tar包

- EXPORT只和-P配合使用才有用

    - -p 会覆盖EXPOSE

```yaml
FROM sunrisenan/nginx:v1.12.2
ADD index.html /usr/share/nginx/html/index.html
EXPOSE 80 # 可选

```

## RUN/ENV

```yaml
FROM centos:7
ENV VER 9.11.4
 # 环境变量
RUN yum install bind-$VER -y 

```

## CMD/ENTRYPOINT

## CMD

- CMD ["executable","param1","param2"] (exec form, this is the preferred form)

    - 非shell模式. 而是类似exec执行, 用C起一个进程.

    - 如果一定要shell模式 -- CMD ["/bin/bash", "-c", "echo 'hello cmd!'"]

    - 第一个参数必须是命令的全路径才行

    - 会被run覆盖,会被entrypoint 覆盖

- CMD ["param1","param2"] (as default parameters to ENTRYPOINT)

- CMD command param1 param2 (shell form) -- /bin/sh -c

```text
FROM centos:7
RUN yum install httpd -y
CMD ["httpd","-D","FOREGROUND"]    # 让其前台运行

```

## ENTRYPOINT

- ENTRYPOINT ["executable", "param1", "param2"] (exec form, preferred)

    - 在shell下执行

    - run命令后面作为entrypoint的参数

    - cmd也作为entrypoint的参数

    - run无法覆盖, 覆盖可以用--entrypoint

- ENTRYPOINT command param1 param2 (shell form)

    - shell默认 cmd和run 参数不生效.

    - 推荐第一种用法.

```shell
FROM centos:7
ADD entrypoint.sh /entrypoint.sh
RUN yum install epel-release -q -y && yum install nginx -y
ENTRYPOINT /entrypoint.sh # 默认会执行这个.
```

# 网络模型



