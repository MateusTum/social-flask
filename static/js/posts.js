function deletePostItem(postId) {
  var listItem = document.getElementById(postId);
  if (listItem) {
      listItem.parentNode.removeChild(listItem);
  }
}

$(document).ready(function() {
    $(document).on('click', '.like-post-btn', function(event) {
      let likesDiv = $(this).closest("div");
      let likeCountElement = likesDiv.find(".likeCount");
      let clickedElement = $(event.currentTarget);
      let postId = clickedElement.data('post-id');

      $.ajax({
        type: "POST",
        url: baseLikeUrl + '?post_id=' + postId,
        data: { post_id: postId },
        success: function (response) {
          console.log((response.liked ? "Liked post " : "Unliked post ") + postId);
          var newSvgElement = $(
            '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="' +
              (response.liked ? "red" : "currentColor") +
              '" class="follow-svg bi bi-star-fill likeImage ' +
              (response.liked ? "liked pop-up-animation-like" : "pop-up-animation-unlike") +
              '" viewBox="0 0 16 16">' +
              '<path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"></path>' +
              "</svg>"
          );
          likesDiv.find(".likeImage").replaceWith(newSvgElement);
  
          var newLikeCountElement = $("<span>")
            .addClass("likeCount")
            .text(response.likes);
          likeCountElement.replaceWith(newLikeCountElement);
        },
      });
  });
});



$(document).on('click', '.delete-post', function(e) {
      e.preventDefault();
      var postId = $(this).data('post-id');
      var isConfirmed = confirm('Are you sure you want to delete this post?');

      if (isConfirmed) {
          $.ajax({
              url: '/posts/delete-post/' + postId,
              method: 'POST',
              data: { postId: postId },
              success: function (response) {
                  console.log(response);
                  alert('Post deleted successfully');
                  deletePostItem("post-" + postId);
              },
              error: function (error) {
                  console.error(error);
                  alert('Error deleting post');
              }
          });
      }
  });

document.addEventListener("DOMContentLoaded", function () {
  console.log("JavaScript is working!");
});
