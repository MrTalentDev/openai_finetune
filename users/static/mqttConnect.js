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
    console.log('reconnecting:', error);
});

client.on('disconnect', (error) => {
    console.log('disconnecting:', error);
});

client.on('error', (error) => {
    console.log('Connection failed:', error);
});

client.on('message', (topic, message) => {
  console.log('receive message：', topic, message.toString())
  if (topic==="django/updated/setting/"+email) {
    alert(JSON.parse(message).body);
    var btn = document.getElementById('updatebtn');
    var doc = document.getElementById('doc_url');
    btn.disabled= false
    doc.disabled= false;
  }
  else if (topic==="django/response/setting/"+email) {
    if (JSON.parse(message).code === '200')
      alert(JSON.parse(message).body);
  }
  else if (topic==="django/progress/setting/"+email){
    // alert(message.toString())
    inc(message.toString())
  }
});

var topic="django/request/setting";

client.subscribe("django/response/setting/"+email); //receive response to update request
client.subscribe("django/updated/setting/"+email); //receive model id after fine-tune finished
client.subscribe("django/progress/setting/"+email); //receive progressive value

//notice this is printed even before we connect
console.log("django/response/setting/"+email);

function inc(width) {
  interval = width == 100 ? 300 : 30000
  var id = setInterval(frame, interval);
  function frame() {
    var pro = document.getElementById('progress').style.width;
    var pros =parseInt(pro)
    if (++pros > width) {
      clearInterval(id);
    } else {
      $('.progress-bar').width(pros+'%');
      $('.progress-bar').text(pros+'%');
      localStorage.setItem('progress', width)
    }
  } 
}