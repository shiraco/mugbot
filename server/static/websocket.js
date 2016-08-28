   $(document).ready(function() {
     if (!window.console) window.console = {};
     if (!window.console.log) window.console.log = function() {};

     console.log("ready");
     wsStart();
   });

   var ws = null;
   var retry_attempts = 0;
   var max_retry_attempts = 120;

   var scheme = "wss";
   var url = scheme + '://' + location.host + '/ws';

   var wsStart = function() {

     if (ws === null) {

       ws = new WebSocket(url);
       console.log(url);

       // onopen
       ws.onopen = function() {
         console.log('onopen');

       };

       // onmessage
       ws.onmessage = function(event) {
         console.log('onmessage');

         // reset the tries back to 0 since we have a new connection opened.
         retry_attempts = 0;

       };

       // onclose
       // When tablet page closed.
       ws.onclose = function(event) {
         console.log('onclose. reason: %s', event.reason);

         if (retry_attempts < max_retry_attempts) {
           // Connection has closed so try to reconnect.
           retry_attempts++;
           ws = null;

           // retry
           wsStart();
           console.log("retry_attempts: ", retry_attempts);

         } else {
           console.log("websocket closed by over max_retry_attempts: ", retry_attempts);

         }

       };

       // onerror
       // When error occurred.
       ws.onerror = function(event) {
         console.log('onerror');

       };

     }
   };
