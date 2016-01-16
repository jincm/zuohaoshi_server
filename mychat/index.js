var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var redis = require("redis");

//var client = redis.createClient(6379,'127.0.0.1',{connect_timeout:3});
var client = redis.createClient(6379,'127.0.0.1');
client.on('error',function(error){
	console.log(error);
});
var sub = redis.createClient();
var pub = redis.createClient();
sub.subscribe('chat');

console.log("redis connected");
//get & set example
/*
client.set('roban', 'this is an testing val', function(err, response) {
	if (err) {
		console.log('Failed to set key of roban, error:' + err);
		return false;
	}

	client.get('roban',function(errGet,responseGet){
		console.log('Val:'+responseGet);
	});

});*/

app.get('/', function(req, res){
	res.send('<h1>Welcome Realtime Server</h1>');
});

var onlineUsers = {};
var onlineCount = 0;

io.on('connection', function(socket){
	console.log('a user connected');
	
	//someone login
	socket.on('login', function(obj){
		socket.name = obj.userid;
		
		//should set redis
		if(!onlineUsers.hasOwnProperty(obj.userid)) {
			onlineUsers[socket.name] = socket;
			onlineCount++;
		}

		pub.publish('group', {msg: 'user joined',onlineUsers:onlineUsers, onlineCount:onlineCount, user:obj});
		//if group,maybe done it
		//io.emit('login', {onlineUsers:onlineUsers, onlineCount:onlineCount, user:obj});
		console.log(socket.name + ' add chat ' + onlineUsers[obj.userid] + ' socketid is ' + socket.id);

		//sub.subscribe('to_' + socket.name);

		client.smembers('msg_' + socket.name,function (err, msgs) {
			console.log("my msgs " + msgs + " msgs_key is " + socket.name);
			for (var i = 0;i < msgs.length; i++) {
				console.log("onemsg is " + msgs[i]);
				msg = JSON.parse(msgs[i]);

				//delete the msg from redis
				client.srem('msg_' + msg.targetId, msgs[i]);

				//console.log("onemsg is " + msg.senderId);
				socket.emit('msg_server',msg, function(result) {
					console.log("user login, msgs to client result is " + result);
					if(result == 'rcv_ok') {
						console.log("msg send ok,delete it from redis:" + JSON.stringify(msg));
					} else {
						//save the msg to redis
						client.sadd('msg_' + msg.targetId, JSON.stringify(msg));//msg is not the true msg?
					}
				});
				//io.to(onlineUsers[socket.name]).emit('msg_server', msg, function (result) {
				//	console.log("msg client result is " + result);
				//});
			}
		});
	});
	
	//
	socket.on('disconnect', function(){
		//should do with redis
		if(onlineUsers.hasOwnProperty(socket.name)) {
			//
			var obj = {userid:socket.name, username:onlineUsers[socket.name]};
			delete onlineUsers[socket.name];
			onlineCount--;

			pub.publish('group', {msg: 'user logout',onlineUsers:onlineUsers, onlineCount:onlineCount, user:obj});
			//io.emit('logout', {onlineUsers:onlineUsers, onlineCount:onlineCount, user:obj});
			console.log(socket.name + ' exit chat');
			//io.emit('user disconnected');
		}
	});

	sub.on('message', function (channel, message) {
		//console.log("channel is " + channel + " targetid is " + message.targetId + " msg is " + message);
		msg = JSON.parse(message);
		console.log("channel is " + channel + " targetid is " + msg.targetId + " msg is " + message);

		//io.sockets.socket(socketid).emit('message', 'for your eyes only');
		//io.sockets.connected[socketid].emit() 或者 io.to(socketId).emit()
		if(onlineUsers.hasOwnProperty(msg.targetId)) {
			if(socket.name == msg.targetId && msg.targetId != msg.senderId ){
				console.log("server redirect msg is " + JSON.stringify(msg));
				//console.log("io.sockets.connected is " + io.sockets.connected);
				//console.log(onlineUsers);
				//console.log(socket.name);
				//io.sockets.sockets
				//var toSocket = _.findWhere(io.sockets.sockets,{id:msg.targetId});
				//io.sockets.connected[msg.targetId]
				onlineUsers[msg.targetId].emit('msg_server', msg , function (result) {
					console.log("msg client result is " + result);
					if(result == 'rcv_ok'){
						//save the msg to redis
						//client.sadd('msg_' + msg.targetId, message);
					} else {
						//save the msg to redis
						console.log("save1 the msg to redis: " + result);
						client.sadd('msg_' + msg.targetId, message);
					}
				});
			}
		} else {
			//save the msg to redis
			console.log("save2 the msg to redis: ");
			client.sadd('msg_' + msg.targetId, message);
		}
	});

	//sender send one msg to someone
	socket.on('msg_client', function(msg,fn) {
		//publish to chat or group
		pub.publish('chat', JSON.stringify(msg));
		//io.emit('msg_server', msg);
		console.log('msg_client is ' + JSON.stringify(msg));
		console.log(msg.senderId + ' say to ' + msg.targetId + " msg is " + msg.content);
		fn("send_ok");
		//confirm to sender msg received
		//console.info("confirm to sender that msg received");
		//io.emit('send_ok', obj);
		//fun("send_ok");
	});

	//receiver confirm msg is received
	/*socket.on('rcv_ok', function(obj) {
		console.debug("receiver confirm msg is received");
	})*/

  
});

http.listen(3000, function(){
	console.log('listening on *:3000');
});
