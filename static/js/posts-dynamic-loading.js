var loadMore = true;
let page = 1;
let isLoading = false;

function buildApiUrl() {
  var queryParams;
  if (currentFeed === "profileTextFeed") {
    queryParams = new URLSearchParams({
      page,
      isUserProfile,
      profileUsername,
    });
  } else if (currentFeed === "profileChaptersFeed" || currentFeed === "profilePicturesFeed") {
    queryParams = new URLSearchParams({
      page,
      profileUsername,
      isFeedPictures,
    });
  } else {
    queryParams = new URLSearchParams({ page });
  }
  return "/posts/load-posts?" + queryParams;
};

function loadContent(elementID) {
  if (isLoading) {
    return;
  }

  isLoading = true;

  var apiUrl = buildApiUrl();
  
  $.ajax({
    url: apiUrl,
    method: "GET",
    success: function (response) {
      if (response.last_page == false) {
        $(elementID).append(response.content);
        console.log("Loading more posts. Current page:", page);
        page++;
        hideLoadingOverlay();
        isLoading = false;
      } else {
        $(elementID).append(response.content);
        console.log("Last posts loaded, no more posts to load");
        loadMore = false;
        hideLoadingOverlay();
        isLoading = false;
      }
    },
    error: function (error) {
      console.error("Error loading posts:", error);
    }, 
  });
};

function debounce(func, delay) {
  let timeoutId;
  return function () {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(func, delay);
  };
};

$(document).ready(function () {
  showLoadingOverlay();
  loadContent(elementID);
  $(window).scroll(debounce(function () {
    if ($(window).scrollTop() + $(window).height() >= $(document).height() - 50 && loadMore) {
      showLoadingOverlay();
      console.log('Loading content...');
      loadContent(elementID);
    }
  }, 1000));
});