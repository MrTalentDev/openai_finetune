// connection option
const email = $("#userinfo").text().trimStart();
const options = {
    clean: true, // retain session
    connectTimeout: 4000, // Timeout period
    reconnectPeriod: 1000,
    // Authentication information
    clientId: 'emqx_test'+email,
    username: '',
    password: '',
};
const connectUrl = 'wss://broker.emqx.io:8084/mqtt';
const client = mqtt.connect(connectUrl, options);
client.on("connect",function(){	
    console.log("connected  "+ client.connected);
});
client.on('reconnect', (error) => {
    console.log('reconnecting:', error)
});

client.on('disconnect', (error) => {
    console.log('disconnecting:', error)
});

client.on('error', (error) => {
    console.log('Connection failed:', error)
});

client.on('message', (topic, message) => {
  console.log('receive message：', topic, message.toString())
  if (topic==="django/updated/setting/"+email) {
    alert("Your resueste completed succefully. "+message.toString())
  }
  else if (topic==="django/response/setting/"+email) {
    alert("Your resueste delivered succefully. ")
  }
});

var topic="django/request/setting";

// console.log("///////subscribing to topics");

// client.subscribe(topic); //single topic
client.subscribe("django/response/setting/"+email); //single topic
client.subscribe("django/updated/setting/"+email); //single topic
// client.subscribe("django/response/setting/"+email); //single topic

//notice this is printed even before we connect
console.log("django/response/setting/"+email);
