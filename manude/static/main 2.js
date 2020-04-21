let skip = false;

$(document).ready(function(){
    $("a").on("mousedown", function (e) {
        skip = true;
        alert($(this).css());
        alert($(this).css("href"));
        document.location.href = $(this).css("href");
    });
    $(document).on('mousedown', function (e) {
        if (skip != true) {
            var start = {x: e.pageX, y: e.pageY}, end;
            $(document).on('click', function (a) {
                end = {x: a.pageX, y: a.pageY};
                if (start.y == end.y) {
                    let height = Math.ceil($(".cursor").css("height").replace("px", ""));
                    let width = Math.ceil($(".cursor").css("width").replace("px", ""));
                    let x_max = start.x + Math.ceil(width/2);
                    let x_min = start.x - Math.ceil(width/2);
                    let y_max = start.y + Math.ceil(height/2);
                    let y_min = start.y - Math.ceil(height/2);

                    (async () => {
                      const rawResponse = await fetch('/take', {
                        method: 'POST',
                        headers: {
                          'Accept': 'application/json',
                          'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                          m: x_min + "-" + y_min + "-" + x_max + "-" + y_max,
                          p: photo,
                        })
                      });
                      await rawResponse.json();
                      window.location = "/";
                    })();
                }
                if (start.y < end.y) {
                    if ((end.y - start.y) > 60) {
                        $('.cursor').css({
                            height: (end.y - start.y) + "px",
                            width: (end.y - start.y) / 2 + "px"
                        });
                    }
                }

            })
        }
    });
    $(window).on('mousemove', function(e) {
        $('.cursor').css({
            top: e.pageY - Math.floor($(".cursor").css("height").replace("px", "")/2) + 'px',
            left: e.pageX - Math.floor($(".cursor").css("width").replace("px", "")/2) + 'px',
        })
    });
});
