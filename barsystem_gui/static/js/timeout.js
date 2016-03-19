var timeout_max = 60;
$(document).ready(function()
{
    var idle_time = 0;
    //Increment the idle time counter every minute.
    var idle_interval = setInterval(timer_increment, 1000);

    function timer_increment() {
        idle_time = idle_time + 1;
        set_count();
        if (idle_time >= timeout_max) { // 1 minute
            location.href = $('#btn-cancel').attr('href');
        }
    }
    function set_count()
    {
        $('#timeout-count').text(idle_time >= 5 ? 'Idle: ' + (timeout_max - idle_time) + 's' : '');
    }

    function reset_timeout(e)
    {
        idle_time = 0;
        set_count();
    }

    //Zero the idle timer on mouse movement.
    $(this).mousemove(reset_timeout);
    $(this).keypress(reset_timeout);
});
