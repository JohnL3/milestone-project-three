// basic set up of socketio and message to say its working
let socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
socket.on('connect', function(){
    socket.emit('message',{'message': 'Up and running'});
});

socket.on('message', function(msg){
      console.log(msg);
  });

socket.on('leaders', function(json){
  console.log(json.data);
  
  let data = json.data;
  let lead = $('.all-leaders');
  lead.html('');
   
  for (let item in data) {
    let user, score;
     [user, score] = data[item];

    let l_div = `<div class="username">
    <span>`+(+item +1)+`</span>
    <span>`+user+`</span>
    <span>`+score+`</span>
    </div>`;

     $('.all-leaders').append(l_div);
  }
  
});
/*********************************************************************************************/

$('#burger').click(function(){

   if($('aside').css('left') === '-245px') {
        $('aside').animate({left: '0'})
   } else {
       $('aside').animate({left: '-245px'})
   }
});

$( window ).resize(function() {
  if($(window).width() > 657) {
	  $('aside').css('left','0');
  } else {
	  $('aside').css('left','-245px');
  }
});