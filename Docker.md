# Docker

> *Use docker to deploy your projects.*

#### what is docker?

___

#### The advantages of docker

___

#### Docker VS Virtual Machine

___

#### How to use Docker?

1. [Install Docker](techi)

   ```shell
   # 1.Uninstalled old version
   $ sudo apt-get remove docker docker-engine docker.io containerd runc
   
   # 2.Set up repository
   # update apt package index
   $ sudo apt-get update
   $ sudo apt-get install \
       apt-transport-https \
       ca-certificates \
       curl \
       gnupg-agent \
       software-properties-common
   # Add Docker’s official GPG key
   $ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
   # set up docker repository
   # i don't recommend to use official repository
   $ sudo add-apt-repository\
      "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) \
      stable"
   
   # 3.Install docker
   $ sudo apt-get update
   $ sudo apt-get install docker-ce docker-ce-cli containerd.io
   
   # 4.Verify that docker engine is installed correct
   $ sudo docker run hello-world
   ```

   <img src="./imgs/docker.png" align="center" width="600px">

```py
1.pull from library/hello-world
2.the docker daemon pulled the "hello-world" img from the docker hub
3.the docker daemon created a new container from that image which runs the executable
4.the docker daemon streamed output to the docker client
```

<img src="./imgs/docker2.jpg" align="center" width="600px">

2.[Docker Commands](techi)

```shell

```





