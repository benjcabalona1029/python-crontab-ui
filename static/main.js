$(document).ready(function () {
    $("#add_job").click(function () {
        $('.ui.modal').modal('show');
    });

    $(".ui.inverted.red.button").click(function () {
        if (confirm('Are you sure you want delete this job?')) {
            const id = $(this).val();
            $.ajax({
                url: `job/${id}/`,
                type: 'DELETE',
                contentType: 'application/json',
            });
            alert("Job Deleted!. Please Reload")
        }


    });

    $(".ui.grey.basic.button").click(function () {
        if (confirm('Are you sure you want run this job?')) {
            const id = $(this).val();
            $.ajax({
                url: `/run_job/${id}/`,
                type: 'GET',
                contentType: 'application/json',
            });

            alert("Job is executed")
        }

    });

    $("#save").click(function () {

        const command = $("#command").val();
        const command_name = $("#command_name").val();
        const schedule = $("#schedule").val();

        if (command === "" || command_name === "" || schedule === "") {
            alert("You must fill out all fields")
        } else {
            $.ajax({
                url: '/create_job/',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    "command": command,
                    "name": command_name,
                    "schedule": schedule
                }),
                statusCode: {
                    404: function (responseObject, textStatus, jqXHR) {
                        // No content found (404)
                        // This code will be executed if the server returns a 404 response
                        alert("Make sure the cron expression is valid.")
                    },
                },
                dataType: 'json',
            });
        }

        $('.ui.modal').modal('hide');

    });

    $("#update").click(function () {
        const id = $(this).val();
        const command = $("#command").val();
        const command_name = $("#command_name").val();
        const schedule = $("#schedule").val();

        if (command === "" || command_name === "" || schedule === "") {
            alert("You must fill out all fields")
        } else {
            $.ajax({
                url: `/update_job/${id}/`,
                type: 'PUT',
                contentType: 'application/json',
                data: JSON.stringify({
                    "command": command,
                    "name": command_name,
                    "schedule": schedule
                }),
                statusCode: {
                    500: function (responseObject, textStatus, jqXHR) {
                        // No content found (404)
                        // This code will be executed if the server returns a 404 response
                        alert("Make sure the cron expression is valid.")
                    },
                },
                dataType: 'json'
            });

        }

    });

    $('.custom.button')
        .popup({
            popup: $('.custom.popup'),
            on: 'click',
            inline: true
        });

});
