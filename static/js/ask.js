
var $registerForm = $('#ask');

if($registerForm.length){
  $registerForm.validate({
    rules:{
      title:{
        required: true
      },
      text: {
        required: true
      },
      tags:{
        required: true
      }
    },
    messages:{
      title: {
        required: 'Enter title!'
      },
      text: {
        required: 'Enter text!',
      },
      tags: {
        required: 'Enter tags!'
      }
    },
  });
}
