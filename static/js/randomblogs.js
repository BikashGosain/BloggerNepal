$(document).on('click', '.page-link', function (e) {
    e.preventDefault();

    let url = $(this).attr('href');

    $.get(url, function (response) {
        const newHtml = $(response);

        $('.rb-blog-container').html(
            newHtml.find('.rb-blog-container').html()
        );

        $('.rb-pagination').html(
            newHtml.find('.rb-pagination').html()
        );
    });
});
