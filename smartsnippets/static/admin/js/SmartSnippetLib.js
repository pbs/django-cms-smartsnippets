

var SnippetWidgetRegistry = (function ($) {
    var _self = {
        'widgets': {},
        'variables': {},
        'events': {}
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
        _call_event: function(event_name){
            $.each(_self['events'], function (widget_type, event_data){
                (event_data[event_name] || function(){})();
            });
        },
        initializeVariables: function(variables_ids){
            var vars = _self['variables'];
            if(variables_ids){
                vars = {};
                $.each(variables_ids.filter(function(el){ return el in _self['variables']; }), function(i, var_name){
                    vars[var_name] = _self['variables'][var_name];
                });
            }
            this._call_event('preInit');
            $.each(vars, function (var_name, var_cls) {
               var_cls.init(var_name);
            });
            this._call_event('postInit');
        },
        allValid: function(variables_ids){
            var vars = _self['variables'];
            if(variables_ids){
                vars = {};
                $.each(variables_ids.filter(function(el){ return el in _self['variables']; }), function(i, var_name){
                    vars[var_name] = _self['variables'][var_name];
                });
            }
            this._call_event('preValidate');
            var isValid = true;
            $.each(vars, function (var_name, var_cls) {
               isValid = (var_cls.validate(var_name) && isValid);
            });
            this._call_event('postValidate');
            return isValid;
        },
        registerWidget: function (widget_type, widget_class, events) {
            if (widget_class['init'] && widget_class['validate']){
                _self['widgets'][widget_type] = _self['widgets'][widget_type] || (
                    _self['widgets'][widget_type] = widget_class)
                // register events
                if (widget_class['events'] && !_self['events'][widget_type]){
                    _self['events'][widget_type] = $.extend({}, widget_class['events']);
                }
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
        deregisterAllVariables: function(){
            _self['variables'] = {}
        },
        get_widget_class: function(widget_type){
            var widget_class = _self['widgets'][widget_type];
            if (!widget_class){
                throw new SnippetWidgetError("Widget type " + widget_type + " is not registered.")
            }
            return widget_class;
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
