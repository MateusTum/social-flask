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
  $(".like-post-btn").click(function (event) {
    event.preventDefault();
    const form = $(this).closest("form");
    const postId = form.attr("action").split("/").pop();
    const likeCountElement = form.find(".likeCount");

    $.ajax({
      type: "POST",
      url: form.attr("action"),
      data: form.serialize(),
      success: function (response) {
        // Create a new SVG element based on the response
        var newSvgElement = $(
          '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="' +
            (response.liked ? "red" : "currentColor") +
            '" class="bi bi-star-fill likeImage ' +
            (response.liked ? "liked pop-up-animation-like" : "pop-up-animation-unlike") +
            '" viewBox="0 0 16 16">' +
            '<path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"></path>' +
            "</svg>"
        );
        form.find(".likeImage").replaceWith(newSvgElement);

        // Update the like count element
        var newLikeCountElement = $("<span>")
          .addClass("likeCount")
          .text(response.likes + " Likes");
        likeCountElement.replaceWith(newLikeCountElement);
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
        var form = document.createElement("form");
        form.method = "POST";
        form.action = "/delete-post/" + postId;
        document.body.appendChild(form);
        form.submit();
      }
    });
  });
});

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function demo() {
  for (let i = 0; i < 5; i++) {
    await sleep(i * 1000);
  }
  console.log("Done");
}

function showOverlay(src) {
  const modalImage = document.querySelector("#imageModal img");
  modalImage.src = src;
  $("#imageModal").modal("show");
}

document.addEventListener("DOMContentLoaded", function () {
  console.log("JavaScript is working!");
});
