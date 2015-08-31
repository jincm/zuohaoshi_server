#!/bin/sh

#test for app

HOST="http://127.0.0.1:8000/v1"
num=1

i=0
while [ $i -lt $num ]; do
	echo ""
	echo "########################"
	echo "######get identify code#"
	echo "########################"
	ACCOUT=`date +%s|cut -b '7-11'`
	#get identify_code
	identify_code=`curl -i -X GET $HOST/users/register?accout=1388913$ACCOUT 2>/dev/null | grep identify_code |awk -F' ' '{print $2}'`
	echo "identify_code is "$identify_code

	echo ""
	echo "########################"
	echo "######register##########"
	echo "########################"
	#register and get token object_id
	result=`curl -i -X POST -H "Content-Type: application/json" -d '{"accout":"1388913'$ACCOUT'","identify_code":"'$identify_code'","passwd":"'$identify_code'"}' $HOST/users/register 2>/dev/null`
	TOKEN=`echo $result | awk -F'"' '{print $12}'` && OBJ_ID=`echo $result | awk -F'"' '{print $4}'`
	echo "result is "$result && echo "token is "$TOKEN  && echo "object_id is "$OBJ_ID && echo "accout is ""1388913'$ACCOUT'"

	echo ""
	echo "########################"
	echo "######show user#########"
	echo "########################"
	#show user
	curl -i -X GET $HOST/users/$OBJ_ID?token=$TOKEN
	
	echo ""
	echo "########################"
	echo "######logout############"
	echo "########################"
	#logout
	curl -i -X GET $HOST/users/logout/$OBJ_ID?token=$TOKEN

	echo ""
	echo "########################"
	echo "######login############"
	echo "########################"
	#login and get token object_id
	#fangzhi duoci denglu bug
	TOKEN=`curl -i -X POST -H "Content-Type: application/json" -d '{"accout":"1388913'$ACCOUT'","passwd":"'$identify_code'"}' $HOST/users/login 2>/dev/null | grep 'token' |awk -F':' '{print $2}' |awk -F'"' '{print $2}'`

	echo ""
	echo "########################"
	echo "######show user#########"
	echo "########################"
	#show user
	curl -i -X GET $HOST/users/$OBJ_ID?token=$TOKEN

	echo ""
	echo "########################"
	echo "######activity##########"
	echo "########################"
	#activity
	MYRANDOM=`cat /dev/urandom | head -n 10 | md5sum | head -c 10`
	TYPE="activity"
	URL="$HOST/$TYPE/post?token=$TOKEN"
	echo $URL
	POST_ID=`curl -i -X POST -H "Content-Type: application/json" -d '{"content":"my post '$MYRANDOM'"}' $URL 2>/dev/null| grep 'post_id' |awk -F':' '{print $2}' |awk -F'"' '{print $2}'`
	curl -i -X GET $HOST/$TYPE/$POST_ID?token=$TOKEN

	echo ""
	echo "########################"
	echo "######group#############"
	echo "########################"
	#group
	MYRANDOM=`cat /dev/urandom | head -n 10 | md5sum | head -c 10`
	TYPE="group"
	URL="$HOST/$TYPE/create?token=$TOKEN"
	echo $URL
	POST_ID=`curl -i -X POST -H "Content-Type: application/json" -d '{"group":"my group '$MYRANDOM'"}' $URL 2>/dev/null| grep 'group_id' |awk -F':' '{print $2}' |awk -F'"' '{print $2}'`
	curl -i -X GET $HOST/$TYPE/$POST_ID?token=$TOKEN

    #upload file
    #curl -i -X POST -F "action=upload" -F "file=@/tmp/test.png" $HOST/users/upload?token=$TOKEN

	i=`expr $i + 1`
done
