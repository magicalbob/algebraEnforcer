FROM centos:8

RUN yum install -y python3 \
 && pip3 install flask PyYAML

ENTRYPOINT cd /opt/algebra && ./algebraui.py
