$("#signup_button").click(function () {
    document.getElementById("error_message").innerHTML = '&nbsp';
    first_name = $('#first_name').val();
    last_name = $('#last_name').val();
    email = $('#email').val();
    pass = $('#pass').val();
    re_pass = $('#re_pass').val();

    if(pass.length < 5)
    {
        message = "Password length should be minimum 6 digits long."
        document.getElementById("error_message").innerHTML = message;

    }
    else {

      $.ajax({
        url: '/signup-user/',
      type: "POST",

        data: {
          'first_name': first_name,
          'last_name': last_name,
          'email': email,
          'pass': pass,
          're_pass': re_pass,

        },
        dataType: 'json',
        success: function (data) {
          if (data.status == true) {
            window.location.href = "/warlord_soft/dashboard/";
          }
          else {
            document.getElementById("error_message").innerHTML = data.message;
          }
        }
      }); }

    });

var input = document.getElementById("re_pass");
if (input){
input.addEventListener("keyup", function(event) {
    if (event.keyCode === 13) {
        event.preventDefault();
        document.getElementById("signup_button").click();
    }
});
}

