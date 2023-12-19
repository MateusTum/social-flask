$(document).ready(function () {
  var stickyDivOffset = $(".sticky").offset().top;

  $(window).scroll(function () {
    if ($(window).scrollTop() > stickyDivOffset) {
      $(".sticky").addClass("fixed");
    } else {
      $(".sticky").removeClass("fixed");
    }
  });
});

$(document).ready(function () {
  // Add a click event listener to the like buttons
  $(".like-post-btn").click(function (event) {
    // Prevent the default form submission
    event.preventDefault();

    // Get the form associated with the clicked button
    const form = $(this).closest("form");

    // Get the post ID from the form's action attribute
    const postId = form.attr("action").split("/").pop();

    // Get the like count element using a class selector
    const likeCountElement = form.find(".likeCount");

    // Make an AJAX POST request to the Flask server with the post ID
    $.ajax({
      type: "POST",
      url: form.attr("action"),
      data: form.serialize(), // Serialize the form data
      success: function (response) {
        // Update the like count and liked status
        likeCountElement.text(response.likes + " Likes");
      },
    });
  });
});

document.addEventListener("DOMContentLoaded", function () {
  var deletePostLinks = document.querySelectorAll(".delete-post");

  deletePostLinks.forEach(function (link) {
    link.addEventListener("click", function (event) {
      event.preventDefault();

      var postId = link.getAttribute("data-post-id");
      var confirmation = confirm("Are you sure you want to delete this post?");

      if (confirmation) {
        // Create a form element
        var form = document.createElement("form");
        form.method = "POST";
        form.action = "/delete-post/" + postId;

        // Append the form to the body and submit it
        document.body.appendChild(form);
        form.submit();
      }
    });
  });
});

document.addEventListener("DOMContentLoaded", function () {
  console.log("JavaScript is working!");
});
