var connect_errors = 0;

$(function(){
	connect_websocket();
	$('#connection').click(function()
	{
		if($(this).hasClass('fail'))
		{
			connect_websocket();
		}
	});
});

var websocket_url = 'ws://localhost:1234/ws/index';
function connect_websocket()
{
	// console.debug('connect');
	var sock = new WebSocket(websocket_url);
	sock.onopen = function(evt)
	{
		// console.debug('sock.onopen:', evt);
		$('#connection').removeClass('fail').addClass('ok');
		connect_errors = 0;
	}
	sock.onclose = function(evt)
	{
		// console.debug('sock.onclose:', evt);
		$('#connection').removeClass('ok').addClass('fail');
		connect_errors++;
		if(connect_errors < 5)
			setTimeout(connect_websocket, 1000);
	}
	sock.onmessage = function(evt)
	{
		// console.debug('sock.onmessage:', evt);
		var message = evt.data;
		if(message.match(/^i\d+b$/))
			$('#messageForm')
				.find('input[name=message]').val(message).end()
				.submit();
	}
	sock.onerror = function(evt)
	{
		// console.debug('sock.onerror:', evt);
	}
}