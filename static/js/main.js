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