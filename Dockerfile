ARG IMAGE=containers.intersystems.com/intersystems/iris-community:latest-cd
FROM $IMAGE

USER root

WORKDIR /opt/irisapp
RUN chown -R irisowner:irisowner /opt/irisapp

USER irisowner

# copy files to image
WORKDIR /opt/irisapp
COPY --chown=irisowner:irisowner src src
COPY --chown=irisowner:irisowner iris.script iris.script
COPY --chown=irisowner:irisowner requirements.txt requirements.txt

# install python requirements 
RUN pip3 install --target /usr/irissys/mgr/python/ -r requirements.txt

# run iris.script
RUN iris start IRIS \
    && iris session IRIS < /opt/irisapp/iris.script \
    && iris stop IRIS quietly