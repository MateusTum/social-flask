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
      data: form.serialize(), // Serialize the form data
      success: function (response) {
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
