/**
 * Created by feliciaan on 30/03/15.
 */
$.ready(function(){
    $('.time').each(function() {
        var timeEl = $( this );
        var time = timeEl.text().split(' ').slice(-1)[0].split(':');

        if (timeEl.text().indexOf('closed') < 0) {
            window.setInterval(function () {
                time = my_tick(time);
                if (time !== "closed") {
                    timeS = "closes in " + ("0" + time[0]).slice(-2) + ":" + ("0" + time[1]).slice(-2) + ":" + ("0" + time[2]).slice(-2);
                } else {
                    timeS = "closed"
                }
                timeEl.html(timeS);
            }, 1000);
        }
    });

    function my_tick(time) {
        if (time[2] > 0) {
            time[2] = time[2] - 1;
        } else if(time[1] > 0) {
            time[2] = 59;
            time[1] = time[1] - 1;
        } else if(time[0] > 0) {
            time[1] = 59;
            time[0] = time[0] - 1;
        } else {
            return "closed";
        }
        return time;
    }
}());