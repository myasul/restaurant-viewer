$("#rst-form").submit(function() {

    var modify_type = $("#rst-form").attr("data-modify");
    var field_id = ["#name", "#desc", ];
    var field_names = ["Name", "Description"]

    var i = 0;
    var has_errors = false;
    var error_msg = "";

    while (i < field_id.length) {

        if (!$(field_id[i]).val()) {

            error_msg += field_names[i] + " is required.<br\>";
            has_errors = true;
        }

        i++;
    }

    if ((modify_type == "create") && !$("#image").val()) {

        error_msg += "Image is required.";
        has_errors = true;

    }

    if (has_errors) {

        $("#restaurant-alert").html("<div class='alert alert-danger' role='alert'>" + error_msg + "</div>");

        return false;

    }
    return true;

});

$("#delete-menu").on('show.bs.modal', function(e) {

    var button = $(e.relatedTarget);
    var menu_id = button.data('menu-id');
    var rst_id = button.data('rst-id');

    $("#confirmation-message").html("Are you sure you want to delete " + button.data('name') + "?");
    $("#confirm-delete-menu").attr("data-menu-id", menu_id);
    $("#confirm-delete-menu").attr("data-rst-id", rst_id);

});

$("#confirm-delete-menu").click(function() {

    $.ajax({
        type: "POST",
        url: "/restaurant/" + $("#confirm-delete-menu").attr("data-rst-id") + "/menu/" + $("#confirm-delete-menu").attr("data-menu-id") + "/delete",
        data: "dummydata=dummydata",
        success: function(response) {

            console.log(response);
            window.location.assign("http://localhost:5000/restaurant/" + $("#confirm-delete-menu").attr("data-rst-id") + "/menu");

        },
        error: function(error) {

            console.log(error);

        }

    })

});

$("#delete-rst").on('show.bs.modal', function(e) {

    var button = $(e.relatedTarget);
    var id = button.data('id');

    $("#confirmation-message").html("Are you sure you want to delete " + button.data('name') + "?");
    $("#confirm-delete-rst").attr("data-id", id);

});

$("#confirm-delete-rst").click(function() {

    $.ajax({
        type: "POST",
        url: "/restaurant/" + $("#confirm-delete-rst").attr("data-id") + "/delete",
        data: "dummydata=dummydata",
        success: function(response) {

            console.log(response);
            window.location.assign("http://localhost:5000/restaurants");

        },
        error: function(error) {

            console.log(error);

        }

    })

});

$("#menu-form").submit(function() {

    var field_id = ["#name", "#desc", "#price"];
    var field_name = ["Name", "Description", "Price"];

    var error_msg = "";
    var i = 0;
    var hasError = false;

    while (i < field_id.length) {

        if (!$(field_id[i]).val()) {

            error_msg += field_name[i] + " is required.<br\>";
            hasError = true;

        }

        i++;
    }

    if (!$("input[name='course']").is(':checked')) {

        error_msg += "Course is required.";
        hasError = true;

    }

    if (hasError) {

        $("#menu-alert").html("<div class='alert alert-danger' role='alert>'>" + error_msg + "</div>");
        return false;

    }

    return true;

});