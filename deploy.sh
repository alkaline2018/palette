#!/bin/bash

echo What should the version be?
read VERSION
APP_NAME="alkaline2018/palette"
CONTAINER_NAME="palette"
APP_STATIC_PATH="/app/public"
HOST_IMAGE_PATH="C:\Workspace\VisualStudioProjects\interactive\interactive\image-upload-api"
#HOST_IMAGE_PATH="/"
HOST_PUBLIC_PATH="$HOST_IMAGE_PATH""/public"
HOST_IP="115.85.181.13"
SLEEP_COMMAND="\"while true; do echo 1hour live;sleep 3600; done\""
#RUN_COMMAND="docker run -d --rm -v $HOST_PUBLIC_PATH:$APP_STATIC_PATH --name $CONTAINER_NAME $APP_NAME:$VERSION /bin/bash -c "'"while true; do echo 1hour live;sleep 3600; done"'
#RUN_COMMAND="docker run -d --rm -v $HOST_PUBLIC_PATH:$APP_STATIC_PATH --name $CONTAINER_NAME $APP_NAME:$VERSION"' /bin/bash -c "while true; do echo 1hour live;sleep 3600; done"'
#RUN_COMMAND="run -d --rm -v $HOST_PUBLIC_PATH:$APP_STATIC_PATH --name $CONTAINER_NAME $APP_NAME:$VERSION /bin/bash -c $SLEEP_COMMAND"
RUN_COMMAND="docker run -d --name $CONTAINER_NAME $APP_NAME:$VERSION /bin/bash -c $SLEEP_COMMAND"
#linux localtime 설정 -v 경로 변경 필요
#ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime
#docker run -d --rm -v /etc/localtime:/etc/localtime:ro -v C:\Workspace\VisualStudioProjects\interactive\interactive\image-upload-api\public:/app/public --name palette alkaline2018/palette:0.1.6 /bin/bash -c "while true; do echo 1hour live;sleep 3600; done"
#windows
#docker run -d -e "TZ=Asia/Seoul" --rm -v C:\Workspace\VisualStudioProjects\interactive\interactive\image-upload-api\public:/app/public --name palette alkaline2018/palette:0.1.7 /bin/bash -c "while true; do echo 1hour live;sleep 3600; done"
STOP_COMMAND="docker stop $CONTAINER_NAME"

echo "---------info---------"

echo "APP_NAME:" $APP_NAME
echo "VERSION:" $VERSION
echo "CONTAINER_NAME:" $CONTAINER_NAME
echo "APP_STATIC_PATH:" $APP_STATIC_PATH
echo "HOST_PUBLIC_PATH:" $HOST_PUBLIC_PATH
echo "HOST_IP:" $HOST_IP
#echo "RUN_COMMAND:" $RUN_COMMAND
echo "STOP_COMMAND:" $STOP_COMMAND

#echo stop motion
#read motino
echo "---------build & push---------"

docker build -t $APP_NAME:$VERSION .
$STOP_COMMAND
#run -d --name palette2 alkaline2018/palette:0.1.1 /bin/bash -c "while true; do echo 1hour live;sleep 3600; done"
#$RUN_COMMAND
#docker push $APP_NAME:$VERSION

#echo stop motion
#read motino
echo "---------pull & run---------"
# 아래의 내용은 docker image를 pull 받고 기존 container 를 정지한다. (정지되면 자동 삭제된다.) 이후 다시 run 후 
# container2를 create 해서 env 폴더의 내용을 host에 복사한다. 그리고 container2를 삭제한다.

#ssh root@$HOST_IP "\
#docker pull $APP_NAME:$VERSION && \
#docker stop $CONTAINER_NAME && \
#$RUN_COMMAND "


# 참고용
# docker run -d --rm -v C:\Users\song_e\Desktop\myfile\env:/app/env --name spsp alkaline2018/spsp:0.0.3 /bin/bash -c "while true; do echo 1hour live;sleep 3600; done"
# docker run -d --rm -v $HOST_PATH:$APP_STATIC_PATH --name $CONTAINER_NAME $APP_NAME:$VERSION /bin/bash -c "while true; do echo 1hour live;sleep 3600; done"
# docker create --name $CONTAINER_NAME $APP_NAME:$VERSION
# docker create --name $CONTAINER_NAME2 $APP_NAME:$VERSION
# docker cp spsp2:/app/env C:\Users\song_e\Desktop\myfile
# docker cp $CONTAINER_NAME2:$APP_STATIC_PATH $HOST_SPSP_PATH
# docker rm spsp2