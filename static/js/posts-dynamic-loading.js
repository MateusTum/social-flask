var loadMore = true;
var page = 2;
let isLoading = false;

/**
 * Initializes a scroll event listener to trigger the loading of more content when the user scrolls.
 *
 * When the user scrolls and reaches near the bottom of the page, and if there is more content to load
 * (as indicated by the `loadMore` variable), this function calls the `loadContent` function with the specified
 * element ID.
 *
 * @function
 * @returns {void}
 */
$(document).ready(function () {
  /**
   * Event handler for the scroll event.
   *
   * Checks if the user has scrolled near the bottom of the page and if there is more content to load.
   * If both conditions are met, it calls the `loadContent` function with the specified element ID.
   *
   * @param {Event} event - The scroll event object.
   * @returns {void}
   * @inner
   */
  $(window).scroll(function () {
    if (
      $(window).scrollTop() + $(window).height() >=
        $(document).height() - 200 &&
      loadMore
    ) {
      loadContent(elementID);
    }
  });
});

/**
 * Appends loaded posts to a specified HTML element.
 *
 * This function fetches posts from the server and appends them to the HTML element
 * with the provided ID.
 *
 * @param {string} elementId - The ID of the HTML element to which the posts will be appended.
 * @returns {void}
 */
function loadContent(elementID) {
  /**
   * Append the loaded posts to the specified HTML element.
   *
   * @param {string} elementId - The ID of the HTML element.
   * @returns {void}
   * @inner
   */
  if (typeof isUserProfile !== 'undefined') {
    var queryParams = new URLSearchParams({
      page,
      loadMore,
      isUserProfile,
      profileUsername,
    });
  } else {
    var queryParams = new URLSearchParams({ page, loadMore });
  }
  var apiUrl = "/home?" + queryParams;
  if (isLoading) {
    return;
  }

  isLoading = true;

  $.ajax({
    url: apiUrl,
    method: "GET",
    success: function (response) {
      if (response.last_page == false) {
        $(elementID).append(response.content);
        console.log("Loading more posts");
        page++;
      } else {
        $(elementID).append(response.content);
        console.log("Last posts loaded, no more posts to load");
        loadMore = false;
      }
    },
    error: function (error) {
      console.log("Error:", error);
    },
  });
}
