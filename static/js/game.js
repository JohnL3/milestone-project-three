$('.close-instructions').click(function(){
  $('.game-instructions').css('display','none');
});

$('#burger').click(function(){

   if($('aside').css('left') === '-245px') {
        $('aside').animate({left: '0'})
   } else {
       $('aside').animate({left: '-245px'})
   }
});

let previousData;
let answers = [];

// post subject choice to server which returns a question to be answered
$('.sqr').click(function(e){
  if(!$(this).hasClass('answered')) {
      let clickedOn = $(this).attr('id');
      $(this).css('background','#607D8B')
      console.log(clickedOn);
      let data = {"quest_id": clickedOn};
      let url = 'http://question-answer-johnl3-1.c9users.io/questions';
    
      $.ajax({
        type : 'POST',
        url : url,
        contentType: 'application/json;charset=UTF-8',
        dataType: 'json',
        data : JSON.stringify(data),
        success: function(d){
            console.log('your question',d);
            previousData = d;
            createQA(d,clickedOn);
            $('.q-a-outer').css('display','flex');
        }
      });
  }
});

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
