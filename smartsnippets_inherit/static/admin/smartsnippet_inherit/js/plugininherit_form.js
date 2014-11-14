(function($) {

    _editor = {
        attachItemsEvents: function(){
            var items = $(this.options.snippetItems);
            var variables_urls = this.options.urls.variables;
            var varsBox = $(this.options.variables);
            items.each(function(){
                $(this).click(function(){
                    items.removeClass('selected');
                    $(this).addClass('selected');
                    $.ajax({
                        url: variables_urls,
                        data: {'snippet_plugin': $(this).attr('data-snippet')},
                        success: function (data) {
                            $(varsBox).html(data);
                        }
                    });
                });
            });
        },
        initOpts: function(opts){
            this.options = $.extend(opts, {
                snippets: opts.variables_module + ' .snippets-list',
                snippetItems: opts.variables_module + ' .snippets-list li',
                variables: opts.variables_module + ' .variables-list'
            });
        }
    }

    SnippetVariablesEditor = window.SnippetVariablesEditor || {
        init: function(requiredOpts) {
            _editor.initOpts(requiredOpts);
            _editor.attachItemsEvents();

            $.ajaxSetup({
                global:true,
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": $('input[name="csrfmiddlewaretoken"]').val()
                },
                cache: false,
                error: function(x, e) {
                    if (x.status == 500) {
                        alert('Internel Server Error.');
                    }
                }
            });

        }
    };
})(django.jQuery);
