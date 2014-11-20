

var SnippetWidgetRegistry = (function ($) {
    var _self = {
        'widgets': {},
        'variables': {},
    };

    return {
        initializeVariables: function(){
            $.each(_self['variables'], function (var_name, var_cls) {
               var_cls.init(var_name);
            });
        },
        allValid: function(){
            var isValid = true;
            $.each(_self['variables'], function (var_name, var_cls) {
               isValid = (var_cls.validate(var_name) && isValid);
            });
            return isValid;
        },
        registerWidget: function (widget_type, widget_class) {
            if (widget_class['init'] && widget_class['validate']){
                _self['widgets'][widget_type] = _self['widgets'][widget_type] || (
                    _self['widgets'][widget_type] = widget_class)
            } else {
                throw "init and validate attrs required."
            }
        },
        registerVariable: function(widget_type, variable_id) {
            if (!widget_type in _self['widgets']){
                throw "Widget type " + widget_type + " is not registered."
            }
            if (variable_id in _self['variables']){
                throw "Variable with id " + variable_id + " was already registered."
            }

            _self['variables'][variable_id] = _self['widgets'][widget_type]
        },
        deregisterVariable: function(variable_id){
            delete _self['variables'][variable_id]
        }
    };
})(jQuery || django.jQuery);
