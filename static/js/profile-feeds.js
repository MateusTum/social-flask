$(document).ready(function () {
    
    $("#load-posts-feed").click(function () {
      currentFeed = 'profileTextFeed';
      loadMore = true;
      page = 1;

      showLoadingOverlay();

      var queryParams = new URLSearchParams({
        page,
        isUserProfile,
        profileUsername,
      });

      var apiUrl = "/posts/load-posts?" + queryParams;

      $(elementID).empty();

      $.ajax({
        url: apiUrl,
        method: "GET",
        success: function (response) {
          if (response.last_page == false) {
            hideLoadingOverlay();
            $(elementID).append(response.content);
            console.log("Switching to posts feed. Current page:", page);
            page++;
          } else {
            hideLoadingOverlay();
            $(elementID).append(response.content);
            console.log("Last posts loaded, no more posts to load");
            loadMore = false;
          }
        },
        error: function (error) {
          console.log("Error:", error);
        },
      });
    });


    $("#load-chapters-feed").click(function () {
      currentFeed = 'profileChaptersFeed';
      loadMore = true;
      page = 1;
      isFeedPictures = true;
      showLoadingOverlay();

      var queryParams = new URLSearchParams({
        page,
        profileUsername,
        isFeedPictures,
      });

      var apiUrl = "/posts/load-posts?" + queryParams;

      $(elementID).empty();

      $.ajax({
        url: apiUrl,
        method: "GET",
        success: function (response) {
          if (response.last_page == false) {
            hideLoadingOverlay();
            $(elementID).append(response.content);
            console.log("Switching to chapters feed. Current page:", page);
            page++;
          } else {
            hideLoadingOverlay();
            $(elementID).append(response.content);
            console.log("Last posts loaded, no more posts to load");
            loadMore = false;
          }
        },
        error: function (error) {
          console.log("Error:", error);
        },
      });
    });

  $("#load-pictures-feed").click(function () {
      currentFeed = 'profilePicturesFeed';
      loadMore = true;
      page = 1;
      isFeedPictures = true;
      showLoadingOverlay();

      var queryParams = new URLSearchParams({
        page,
        profileUsername,
        isFeedPictures,
      });

      var apiUrl = "/posts/load-posts?" + queryParams;

      $(elementID).empty();

      $.ajax({
        url: apiUrl,
        method: "GET",
        success: function (response) {
          if (response.last_page == false) {
            hideLoadingOverlay();
            $(elementID).append(response.content);
            console.log("Switching to chapters feed. Current page:", page);
            page++;
          } else {
            hideLoadingOverlay();
            $(elementID).append(response.content);
            console.log("Last posts loaded, no more posts to load");
            loadMore = false;     
          }
        },
        error: function (error) {
          console.log("Error:", error);
        },
      });
    });
  });
