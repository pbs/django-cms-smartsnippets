(function($) {
    $(function() {
        var snippetMenu = $('.snippets-list').first();
        var snippetListItem = snippetMenu.find('li');
        snippetListItem.each(function(){
            $(this).click(function(){
                snippetListItem.removeClass('selected');
                $(this).addClass('selected');
            });
        });
    });
})(django.jQuery);
