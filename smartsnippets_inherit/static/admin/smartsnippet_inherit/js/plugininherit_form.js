(function($) {

    _editor = {
        _initial: {},
        _variablesSubmission: false,
        loadVariables: function () {
            var varsBox = $(_editor.options.variables);
            // mark selected
            $(this).siblings().removeClass('selected');
            $(this).addClass('selected');
            // show variables
            var snippet_plugin = $(this).attr('data-snippet');
            SnippetWidgetRegistry.deregisterAllVariables();
            $.ajax({
                url: _editor.options.urls.variables,
                data: {'snippet_plugin': snippet_plugin},
                success: function (data) {
                    $(varsBox).html(data);
                    SnippetWidgetRegistry.initializeVariables();
                    $(varsBox).find("[name^='_'][name$='_'][id^='var_']").each(function(){
                        var label = (
                            $(varsBox).find('label[for="' + $(this).attr('id') + '"]').text() ||
                            $(this).attr('name').replace(/(^_)|(_$)/g, '')
                        );
                        _editor._initial[snippet_plugin] = (
                            _editor._initial[snippet_plugin] || {}
                        );
                        _editor._initial[snippet_plugin][$(this).attr('name')] = {
                            'label': label,
                            'value': $(this).val()
                        }
                    });

                    $('<input type="submit"/>')
                        .val('Overwrite changed variables')
                        .appendTo($(varsBox))
                        .click(function() {
                            if (!SnippetWidgetRegistry.allValid()){
                                return false;
                            }
                            var changed_vars = [];
                            $.each(_editor._initial[snippet_plugin], function(name, initial){
                                if ($('[name="' + name + '"]').val() != initial['value']){
                                    changed_vars.push(initial['label']);
                                }
                            });
                            _variablesSubmission = true;
                            alert(changed_vars.join(', '));
                            return false;
                        });

                }
            });
        },
        initSnippetPlugins: function(){
            $(this.options.snippetItems).each(function(){
                $(this).click(_editor.loadVariables);
            });
            $('form').submit(function () {
                return !_editor._variablesSubmission;
            });
        },
        initOpts: function(opts){
            this.options = $.extend(opts, {
                snippets: opts.variables_module + ' .snippets-list',
                snippetItems: opts.variables_module + ' .snippets-list li',
                variables: opts.variables_module + ' .variables-list'
            });
        },
        setHeaders: function () {
            $.ajaxSetup({
                global: true,
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
    }

    SnippetVariablesEditor = window.SnippetVariablesEditor || {
        init: function(requiredOpts) {
            _editor.initOpts(requiredOpts);
            _editor.initSnippetPlugins();
            _editor.setHeaders();
        }
    };
})(django.jQuery);
