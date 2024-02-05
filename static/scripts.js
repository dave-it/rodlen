// static/scripts.js



    function setOffset(offset) {
        // Hier verwenden wir Fetch-API, um einen POST-Request an den Flask-Endpunkt zu senden
        fetch('/update_global_offset/'+offset, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            // Konsolenausgabe für Debugging-Zwecke
            console.log(data);

            // Hier können Sie weitere Logik für die Benutzeroberfläche hinzufügen
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

$(document).ready(function() {

    function showAlert(status, message) {
        if (status === 'success') {
            alert(message);
        } else {
            alert('Error: ' + message);
        }
    }

    function startTimer(startNumber) {
        $.ajax({
            url: '/start',
            method: 'POST',
            data: { 'start_number': startNumber },
            success: function(data) {
                console.log("SUCCESS????")
                showAlert(data.status, data.message);
                if (data.status === 'success') {
                    updateTimerOnPage('00:00');
                    // Starte die Aktualisierung der Runtime jede Sekunde
                    // setInterval(function() {
                    //     updateRuntime(startNumber);
                    // }, 1000);
                }
            },
            error: function(error) {
                console.error('Error:', error);
            }
        });
    }

    function updateRuntime(startNumber) {
        // Hier sollte Logik hinzugefügt werden, um die aktualisierte Laufzeit vom Server abzurufen
        // und die Runtime-Zelle auf der Webseite zu aktualisieren
        $.ajax({
            url: '/get_runtime',
            method: 'POST',
            data: { 'start_number': startNumber },
            success: function(data) {
                console.log("HELLO?")
                $('#runtime-' + startNumber).text(data.runtime);
            },
            error: function(error) {
                console.error('Error:', error);
            }
        });
    }

    function updateTimerOnPage(time) {
        $('#timer').text(time);
    }

    // Event-Handler für das Formular mit der ID 'start-form'
    $('#start-form').submit(function(event) {
        event.preventDefault();
        // Logik für das Hinzufügen eines Athleten hier einfügen...
    });

    // Event-Handler für das Klicken auf das Start-Button-Div
    $('.start-button').click(function() {
        var startNumber = $(this).data('start-number');
        startTimer(startNumber);
    });
});
