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
  console.log('receive message：', topic, message.toString());
  console.log("django/progress/setting/"+email);
  msg = JSON.parse(message);
  if (topic==="django/updated/setting/"+email) {
    var btn = document.getElementById('updatebtn');
    var doc = document.getElementById('doc_url');
    btn.disabled= false
    doc.disabled= false;
  }
  else if (topic==="django/response/setting/"+email) {
    if (msg.code === '200')
    console.log(msg.body)
      // alert(msg.body);
  }
  else if (topic==="django/progress/setting/"+email){
    console.log('receive message：', topic, message.toString())
    // $('.progress-bar').width(message.toString()+'%');
    // $('.progress-bar').text(message.toString()+'%');
    inc(message.toString())
    localStorage.setItem('progress', message.toString())
  }
  else if (topic==="django/response/answer/"+email){
    
    if (msg.code === 200){
      let answer = document.getElementById('answer');
      let btn = document.getElementById('sendbtn')
      let question = document.getElementById('question')
      let wait = document.getElementById('container-loading')
      wait.style.display="none"
      btn.disabled= false
      question.disabled= false
      answer.disabled= false
      answer.value = msg.body;
    }
  }
});

var topic="django/request/setting";

client.subscribe("django/response/setting/"+email); //receive response to update request
client.subscribe("django/updated/setting/"+email); //receive model id after fine-tune finished
client.subscribe("django/progress/setting/"+email); //receive progressive value

client.subscribe("django/response/answer/"+email); //receive progressive value

//notice this is printed even before we connect
console.log("django/progress/setting/"+email);

function inc(width) {
  interval = width == 100 ? 100 : 200
  var id = setInterval(frame, interval);
  function frame() {
    var pro = document.getElementById('progress').style.width;
    var pros =parseInt(pro)
    if (++pros > width) {
      clearInterval(id);
    } else {
      $('.progress-bar').width(pros+'%');
      $('.progress-bar').text(pros+'%');
      if (pros === 100){
        $(".progress-bar").css("background-color","#5cb85c");
        alert('Your request successfuly finished')
      }

    }
  } 
}