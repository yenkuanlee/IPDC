# iServStor
FROM ubuntu:16.04
MAINTAINER Docker Newbee yenkuanlee@gmail.com

RUN apt-get -qq update

# Basic tool
RUN apt-get -qqy install sudo
RUN apt-get -qqy install python python-dev
RUN apt-get -qqy install wget
RUN apt-get -qqy install vim
RUN apt-get -qqy install sqlite3
RUN apt-get -qqy install net-tools # ifconfig
RUN apt-get -qqy install python-pkg-resources # iservstor need it, only for ubuntu 14.04

# update java
RUN apt-get -qq update
RUN apt-get -qqy install software-properties-common
RUN add-apt-repository -y ppa:webupd8team/java
RUN apt-get -qqy install openjdk-8-jdk

# for iota
RUN apt-get -qqy install git
RUN apt-get -qqy install python-setuptools
RUN apt-get -qqy install build-essential
RUN easy_install pip

#RUN apt-get -qqy install maven # long time ...
RUN apt-get -qq update

# for mcu
RUN apt-get -qqy install python3.5-dev
RUN apt -qqy install python3-setuptools
RUN easy_install3 pip
RUN add-apt-repository ppa:ethereum/ethereum
RUN apt-get update
RUN apt-get -qqy install solc
RUN pip3 install web3
RUN pip install py-solc
RUN apt-get install -y locales
RUN locale-gen zh_TW zh_TW.UTF-8 zh_CN.UTF-8 en_US.UTF-8
RUN echo 'export LC_ALL=zh_TW.utf8' >> /root/.bashrc

# kevin
RUN pip2 install paho-mqtt
RUN pip3 install paho-mqtt
RUN pip2 install tensorflow
RUN pip3 install tensorflow
RUN chmod 755 /usr/local/bin/pip
RUN chmod 755 -R /usr/local/lib/python*/dist-packages

# tomcat
RUN cd /opt && wget http://www-us.apache.org/dist/tomcat/tomcat-7/v7.0.85/bin/apache-tomcat-7.0.85.tar.gz && tar xzf apache-tomcat-7.0.85.tar.gz&& mv apache-tomcat-7.0.85 tomcat7 && echo 'export CATALINA_HOME="/opt/tomcat7"' >> ~/.bashrc

# somthing need
RUN apt-get -qqy install mosquitto 
RUN apt-get -qqy install mosquitto-clients
RUN apt-get -qqy install psmisc
RUN apt-get -qqy install ant
RUN apt-get -qqy install cmake

# Add localadmin user
RUN useradd -m localadmin && echo "localadmin:openstack" | chpasswd && adduser localadmin sudo
USER localadmin
RUN echo 'export LC_ALL=zh_TW.utf8' >> /home/localadmin/.bashrc

# clone IPDC project and setting
RUN cd && \
git clone https://github.com/yenkuanlee/IPDC

# VOltDB
RUN cd && \
wget https://github.com/VoltDB/voltdb/archive/voltdb-8.0.tar.gz && \
tar -zxf voltdb-8.0.tar.gz && \
mv voltdb-voltdb-8.0/ voltdb && \
cd voltdb && \
ant clean ; ant -Djmemcheck=NO_MEMCHECK && \
echo 'export CLASSPATH="$CLASSPATH:$HOME/voltdb/voltdb/*:$HOME/voltdb/lib/*:./"' >> /home/localadmin/.bashrc && \
echo 'alias voltdb="/home/localadmin/voltdb/bin/sqlcmd"' >> /home/localadmin/.bashrc && \
/home/localadmin/voltdb/bin/voltdb init


USER root
RUN cd /home/localadmin/IPDC && \
cp .ipfs/geth /usr/local/bin && \
chmod 755 /usr/local/bin/pip && \
chmod 755 -R /usr/local/lib/python2.7/dist-packages && \
service mosquitto restart

USER localadmin
RUN cd
