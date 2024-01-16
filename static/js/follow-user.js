$(document).ready(function () {
    // Intercept the form submissions
    $(".follow-form").submit(function (event) {
        // Prevent the default form submission
        event.preventDefault();
        // Reference the form being submitted
        var $form = $(this);
      // Perform AJAX request
      $.ajax({
        type: "POST",
        url: $form.attr("action"),
        data: $form.serialize(),  // Add this line to include form data
        success: function(response) {
          // Update the icon based on the response
          if (response.following_status) {
            $('#followIconContainer').html(
              '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="white" class="follow-svg bi bi-person-check-fill" viewBox="0 0 16 16">' +
                '<path fill-rule="evenodd" d="M15.854 5.146a.5.5 0 0 1 0 .708l-3 3a.5.5 0 0 1-.708 0l-1.5-1.5a.5.5 0 0 1 .708-.708L12.5 7.793l2.646-2.647a.5.5 0 0 1 .708 0" />' +
                '<path d="M1 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6" />' +
              '</svg>'
            );
            $("#followBtn").removeClass("btn-success").addClass("btn-secondary");
          } else {
            $('#followIconContainer').html(
              '<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="white" class="follow-svg bi bi-person-fill-add" viewBox="0 0 16 16">' +
                '<path d="M12.5 16a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7m.5-5v1h1a.5.5 0 0 1 0 1h-1v1a.5.5 0 0 1-1 0v-1h-1a.5.5 0 0 1 0-1h1v-1a.5.5 0 0 1 1 0m-2-6a3 3 0 1 1-6 0 3 3 0 0 1 6 0" />' +
                '<path d="M2 13c0 1 1 1 1 1h5.256A4.5 4.5 0 0 1 8 12.5a4.5 4.5 0 0 1 1.544-3.393Q8.844 9.002 8 9c-5 0-6 3-6 4" />' +
              '</svg>'
            );
            $("#followBtn").removeClass("btn-secondary").addClass("btn-success");
          }
          // Display a message to the user
          console.log(response.message);
        },
        error: function(error) {
          console.log('Error:', error);
        }
      });
    });
  });