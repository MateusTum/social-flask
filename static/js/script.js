$(document).ready(function() {
    var stickyDivOffset = $('.sticky').offset().top;

    $(window).scroll(function() {
        if ($(window).scrollTop() > stickyDivOffset) {
            $('.sticky').addClass('fixed');
        } else {
            $('.sticky').removeClass('fixed');
        }
    });
});

document.addEventListener("DOMContentLoaded", function() {
    console.log("JavaScript is working!");
});

 $(document).ready(function() {
        // Add a click event listener to the like buttons
        $('.like-post-btn').click(function(event) {
            // Prevent the default form submission
            event.preventDefault();

            // Get the form associated with the clicked button
            const form = $(this).closest('form');

            // Get the post ID from the form's action attribute
            const postId = form.attr('action').split('/').pop();

            // Get the like count element using a class selector
            const likeCountElement = form.find('.likeCount');

            // Make an AJAX POST request to the Flask server with the post ID
            $.ajax({
                type: 'POST',
                url: form.attr('action'),
                data: form.serialize(), // Serialize the form data
                success: function(response) {
                    // Update the like count and liked status
                    likeCountElement.text(response.likes + ' Likes');
                }
            });
        });
    });