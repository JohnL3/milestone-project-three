let myAlert = true;
// used for when user clicks to close browser window or tab back
// i need to remove user from user list of other users online
window.onbeforeunload  = function(e) {
    if (myAlert === true) {
        let user = $('#username').text();
        clearScreen();
        let dialoug = 'Clearing your username from server';
        socket.emit('exitgame', user);
        e.returnValue = dialoug;
        return dialoug;
    }
    myAlert = true;
};

// called if browser window is being closed 
function clearScreen() {
  $('#details').text('You closed tab, Need to clear you from online users. If you didnt mean to leave, click HOME link and rejoin.');
  $('.sqr-con').css('display','none');
}

// basic set up of socketio and message to say its working
let socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
socket.on('connect', function(){
    socket.emit('message',{'message': 'Up and running'});
});

socket.on('message', function(msg){
     
  });
  
// when user clicks home this fires exitgame and removes user from user list of all users online
$('.home').on('click', function(){
  let user = $('#username').text();
  
  socket.emit('exitgame', user);
  myAlert = false;
});

// when user clicks leaderboard this fires exitgame and removes user from user list of all users online
$('.my-leader-board').click(function(){
  let user = $('#username').text();
  socket.emit('exitgame', user);
  myAlert = false;
});

//shows users who are online and who leave
socket.on('in_out_game', function(json){
    let online = $('#online-users');
    online.html('');
    let users = json.data;
    
    let user = Object.keys(users);
    
    for (let key in user) {
     let span =`<span class="user usr-name">`+users[user[key]].username+`</span>
        <span class="user usr-score ` + users[user[key]].username + `">`+users[user[key]].score+`</span>`;
        online.append(span);
    }

});

//updates the view of user score for all users online
socket.on('my_score', function(json){
  let score = json.score;
  let user = json.user;
  $('.single.'+user).text(score);
});

//shows the leaderboard
socket.on('leaders', function(json){
  
  //only want top 3 for game page view
  let data = json.data.slice(0,3);
  
  let lead = $('.lead');
  
  lead.html('');
    
    for (let item in data) {
      let ind = '<span class="user lead">'+(+item +1)+'</span>';
       
       let user, score;
       [user, score] = data[item];
       let userSpan = '<span class= "user lead">'+user+'</span>';
       let scoreSpan = '<span class= "user lead usr-score">'+score+'</span>';
       
       $('#leader-board').append(ind, userSpan,scoreSpan);
    }
});
  
/*************************************************************************************************/

$('.close-instructions').click(function(){
  $('.game-instructions').css('display','none');
});

$('#burger').click(function(){

   if($('aside').css('left') === '-245px') {
        $('aside').animate({left: '0'});
   } else {
       $('aside').animate({left: '-245px'});
   }
});

$( window ).resize(function() {
  if($(window).width() > 657) {
	  $('aside').css('left','0');
  } else {
	  $('aside').css('left','-245px');
  }
});


let previousData;
let answers = [];

// post subject choice to server which returns a question to be answered
$('.sqr').click(function(e){
  if(!$(this).hasClass('answered')) {
      let clickedOn = $(this).attr('id');
      $(this).css('background','#607D8B');
      
      let data = {"quest_id": clickedOn};
      let url = 'http://question-answer-johnl3-1.c9users.io/questions';
    
      $.ajax({
        type : 'POST',
        url : url,
        contentType: 'application/json;charset=UTF-8',
        dataType: 'json',
        data : JSON.stringify(data),
        success: function(d){
            
            previousData = d;
            createQA(d,clickedOn);
            $('.q-a-outer').css('display','flex');
        }
      });
  }
});


// post answer to question to server 
$('#ans-button').click(()=>{
  
  let _id = $('.surround').attr('id');
  
  if(Object.getOwnPropertyNames(previousData).length > 2) {
    $('input:checkbox:checked').each(function() {
      answers.push($(this).val());
    });
    
    let answerData = {
      questionId: _id,
      answer: answers
    };
    if(answers.length > 0){
    
    postAnswers(answerData);
    } else {
      $('.error-msg').css('display','flex');
      setTimeout(function(){
        $('.error-msg').css('display','none');
      },3000);
    }
  } else {
    let answers = $('.ans-inp').val().split(/[\\,]\s|[\s\\,]/);
    if(answers != '') {
      let answerData = {
        'questionId': _id,
        'answer': answers
      };
      
      postAnswers(answerData);
    } else {
      $('.error-msg').css('display','flex');
      setTimeout(function(){
        $('.error-msg').css('display','none');
      },3000);
    }
  }
});

function postAnswers(data) {
  let url = 'http://question-answer-johnl3-1.c9users.io/answer';

  $.ajax({
      type : 'POST',
      url : url,
      contentType: 'application/json;charset=UTF-8',
      dataType: 'json',
      data : JSON.stringify(data),
        success: function(d){
        
        $('.q-a-outer').css('display','none');
        $('#section-c').remove();
         if('game-over' in d) {
            setTimeout(function(){
                if (d.msg[0].result === 'correct') {
                  $('#'+d.msg[0].id).addClass('correct answered');
                } else {
                  $('#'+d.msg[0].id).addClass('wrong answered');
                }
                answers = [];
                gameOver();
              },500);
          } else {
              setTimeout(function(){
                if (d.msg[0].result === 'correct') {
                  $('#'+d.msg[0].id).addClass('correct answered');
                } else {
                  $('#'+d.msg[0].id).addClass('wrong answered');
                }
                answers = [];
              },500);
          }
        }
    });
}

function gameOver() {
  setTimeout(function(){
    $('.game-over').css('display','flex');
    let id = $('#username').text();
    let score = $('.'+id).text();
    $('.final-score').text(score);
    if($('.game-over').css('left') === '-1550px') {
        $('.game-over').animate({left: '0'});
   }
  },500);
}

//Display question on page add required elements
function createQA(data, id) {
$('.surround').attr('id', id);

if (Object.getOwnPropertyNames(data).length > 2) {
  
  $('.input-ans').css('display','none');
  $('.question-a').text(data.question);
  $('.question-b').text(data.description);
 
  let divb = '<div id="section-c"></div>';

  $('.surround').append(divb);

  for(let item in data.choices) {
    let span = createAnswerElement(data.choices[item],item);
    $('#section-c').append(span);
  }

} else {
  
  $('.question-a').text(data.question);
  $('.question-b').text(data.description);
  $('.input-ans').css('display','block');
  $('.ans-inp').val('');
}

// used in th createQa function
function createAnswerElement(answer,item) {
      let el =`<div class='answer'>
      <input type="checkbox" class="radio" id="radio-`+item+`" value="`+answer+`">
      <span>`+answer+`</span>
      </div>`;
      return el;
    }

}
