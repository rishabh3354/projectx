$("#login_button").click(function () {
    email = $('#your_email').val();
    pass = $('#your_pass').val();

    document.getElementById("error_message").innerHTML = 'Checking details...';

    var urlString = window.location.href;
    urlParams = parseURLParams(urlString);
    if (urlParams){
        redirect = urlParams["next"][0]
    }
    else{
        redirect = null
    }

    console.log(urlParams);

      $.ajax({
        url: '/login-request/',
      type: "POST",

        data: {
          'your_email': email,
          'your_pass': pass,

        },
        dataType: 'json',
        success: function (data) {
          if (data.status == true) {
                if(redirect){
                    window.location.href = redirect;
                }
                else{
                    window.location.href = data.redirect_url;
                }

          }
          else {
            document.getElementById("error_message").innerHTML = data.message;
          }
        }
      });

    });

function parseURLParams(url) {
    var queryStart = url.indexOf("?") + 1,
        queryEnd   = url.indexOf("#") + 1 || url.length + 1,
        query = url.slice(queryStart, queryEnd - 1),
        pairs = query.replace(/\+/g, " ").split("&"),
        parms = {}, i, n, v, nv;

    if (query === url || query === "") return;

    for (i = 0; i < pairs.length; i++) {
        nv = pairs[i].split("=", 2);
        n = decodeURIComponent(nv[0]);
        v = decodeURIComponent(nv[1]);

        if (!parms.hasOwnProperty(n)) parms[n] = [];
        parms[n].push(nv.length === 2 ? v : null);
    }
    return parms;
}

var input = document.getElementById("your_pass");
if(input){
input.addEventListener("keyup", function(event) {
    if (event.keyCode === 13) {
        event.preventDefault();
        document.getElementById("login_button").click();
    }
});
}
