

var SnippetWidgetRegistry = (function ($) {
    var _self = {
        'widgets': {},
        'variables': {},
    };


    function SnippetWidgetError(message){
            this.level = "Error";
            this.htmlMessage = "Error detected." + message;
            this.message = message;
            this.name = 'SnippetWidgetError';
            this.toString = function(){
                return this.name + ": " + this.message;
            }
    }

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
                throw new SnippetWidgetError("init and validate attrs required.")
            }
        },
        registerVariable: function(widget_type, variable_id) {
            if (!_self['widgets'][widget_type]){
                throw new SnippetWidgetError("Widget type " + widget_type + " is not registered.")
            }
            if (_self['variables'][variable_id]){
                throw new SnippetWidgetError("Variable with id " + variable_id + " was already registered.")
            }

            _self['variables'][variable_id] = _self['widgets'][widget_type]
        },
        deregisterVariable: function(variable_id){
            delete _self['variables'][variable_id]
        },
        get_variables: function(widget_type){
            vars_ids = []
            if (!widget_type){
                return vars_ids;
            }
            $.each(_self['variables'], function (var_name, var_cls) {
                if(_self['widgets'][widget_type] === var_cls){
                   vars_ids.push(""+ var_name);
                }
            });
            return vars_ids;
        }
    };
})(jQuery || django.jQuery);
