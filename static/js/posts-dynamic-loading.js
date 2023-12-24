var loadMore = true;
var page = 2;

$(document).ready(function() {
    $(window).scroll(function() {
        if ($(window).scrollTop() + $(window).height() >= $(document).height() - 200 && loadMore) {
            demo();
            loadContent();
            demo();
        }
    });
});

function loadContent() {
    const queryParams = new URLSearchParams({ page, loadMore });
    var apiUrl = '/home?' + queryParams;

    $.ajax({
        url: apiUrl,
        method: 'GET',
        success: function(response) {
            if (response.last_page == false) {
                $('#feed-posts').append(response.content);
                console.log('Loading more posts');
                console.log(page);
                page++;

            } else {
                $('#feed-posts').append(response.content);
                console.log('No more posts to load');
                loadMore = false;
            }
        },
        error: function(error) {
            console.log('Error:', error);
        }
    });
}