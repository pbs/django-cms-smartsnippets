(function($) {
    $(document).ready(function(){
        $('.field-box.field-predefined_widgets').each(function(){
            if ($(this).find('ul.predefined-widgets li').length === 0){
                $(this).hide();
            }
        });
    });
}(django.jQuery));


function populateWidgetResources(predefined_widget_el){
    (function($) {
        var inline = $(predefined_widget_el).parents('.inline-related').first();

        var widget_type = $(predefined_widget_el).attr('data-widget');
        var widget_resources = $(predefined_widget_el).attr('data-resources');

        var widget_select = inline.find('.field-widget').find('select').first();
        var resources = inline.find('.field-resources').find('textarea').first();

        if (widget_select.length > 0 && widget_type.length > 0){
            widget_select.val(widget_type);
        }
        if (resources.length > 0 && widget_resources.length > 0){
            resources.val(widget_resources);
        }
    }(django.jQuery));
}
