(function($) {

    _editor = {
        _initial: {},
        _variablesSubmission: false,
        getInfoBox: function(text, type){
            return "<div class='ssvar-info alert alert-block " + (type? 'alert-' + type: '') + "'>" + text + "</div>";
        },
        getVariablesEl: function(){
            return $(this.options.variables)
                .find("[name^='_'][name$='_'][id^='var_']");
        },
        getVariableLabel: function(varEl){
            var varsBox = $(this.options.variables);
            return (
                varsBox.find('label[for="' + varEl.attr('id') + '"]').text() ||
                varEl.attr('name').replace(/(^_)|(_$)/g, '')
            );
        },
        variablesToString: function(varsEl){
            var self = this;
            return $.map(varsEl, function(el){
                return self.getVariableLabel($(el));
            }).join(', ');
        },
        registerInitialData: function(snippetId){
            var self = this;
            self._initial[snippetId] = {};
            self.getVariablesEl().each(function(){
                self._initial[snippetId][$(this).attr('name')] = $(this).val();
            });
        },
        submitOverwriteData: function(snippetId){
            var self = this;
            return function() {
                var varsBox = $(self.options.variables);
                if (!SnippetWidgetRegistry.allValid()){
                    return false;
                }
                var post_data = {'snippet_plugin': snippetId};
                var varsEl = [];
                $.each(self._initial[snippetId], function(name, initial_value){
                    var varEL = $('[name="' + name + '"]');
                    var current_value = varEL.val();
                    if (initial_value != current_value){
                        varsEl.push(varEL);
                        post_data[name] = current_value;
                    }
                });
                if (varsEl.length === 0){
                    alert('No variables changed');
                    return ;
                }
                var answer = confirm(
                    "The following variables will be overwritten: " +
                    self.variablesToString(varsEl) +
                    ". Are you sure?"
                );
                if(!answer){
                    return ;
                }
                self._variablesSubmission = true;
                varsBox.html(self.getInfoBox("Saving variables...", "warning"));
                $.ajax({
                    url: self.options.urls.variables,
                    data: post_data,
                    type: 'POST',
                    success: function (data) {
                        varsBox.html(self.getInfoBox('Variables saved.', 'success'));
                    },
                    error: function(){
                        varsBox.html(self.getInfoBox('Error occured while saving variables.', 'error'));
                    },
                    complete: function(){
                        self._variablesSubmission = false;
                        self.resizeIframe();
                    }
                });
                return false;
            };
        },
        resetToOriginalVariables: function(snippetId){
            var self = this;
            return function() {
                var answer = confirm(
                    "Are you sure you want to reset variables? You will " +
                    "loose all overwritten variables for this smartsnippet " +
                    "plugin?"
                );
                if (!answer){
                    return ;
                }
                var varsBox = $(self.options.variables);
                varsBox.html(self.getInfoBox("Reseting variables to original values...", "warning"));
                $.ajax({
                    url: self.options.urls.variables,
                    data: {'snippet_plugin': snippetId},
                    type: 'DELETE',
                    success: function (data) {
                        varsBox.html(self.getInfoBox('Variables were reset to their original values.', 'success'));
                    },
                    error: function(){
                        varsBox.html(self.getInfoBox('Error occured while reseting variables.', 'error'));
                    },
                    complete: function(){
                        self._variablesSubmission = false;
                        self.resizeIframe();
                    }
                });
            };
        },
        resetToInitialVariables: function(snippetId){
            return function(){ _editor.loadVariables(snippetId);};
        },
        loadVariables: function (snippetId) {
            var self = _editor;
            SnippetWidgetRegistry.deregisterAllVariables();
            // show variables
            var varsBox = $(self.options.variables);
            $(varsBox)
                .html(self.getInfoBox("Loading variables...", "warning"))
                .toggleClass('bg-empty', varsBox.is(':empty'));
            $.ajax({
                url: self.options.urls.variables,
                data: {'snippet_plugin': snippetId},
                success: function (data) {
                    $(varsBox).html('<table>' + data + '</table>')
                        .append(
                            $("<div />").addClass("form-actions no-background").append(
                                $('<button type="button"/>')
                                    .addClass('submit-row btn btn-light')
                                    .html('<i class="ace-icon fa fa-undo" />' +
                                          'Revert to original ' +
                                          self.options.plugin_name)
                                    .click(self.resetToOriginalVariables(snippetId)),

                                $('<button type="button" />')
                                    .addClass('submit-row btn cancel-btn')
                                    .html('<i class="ace-icon fa fa-remove" />' +
                                          'Cancel Changes')
                                    .click(self.resetToInitialVariables(snippetId)),

                                $('<button type="button" />')
                                    .addClass('submit-row btn btn-primary')
                                    .html('<i class="ace-icon fa fa-check" />' +
                                          'Save Changes')
                                    .click(self.submitOverwriteData(snippetId))
                            )
                        );
                    SnippetWidgetRegistry.initializeVariables();
                    self.registerInitialData(snippetId);
                    varsBox.toggleClass('bg-empty', varsBox.is(':empty'));
                },
                error: function(){
                    $(varsBox)
                        .html(self.getInfoBox("Error loading variables", "error"))
                        .toggleClass('bg-empty', varsBox.is(':empty'));
                },
                complete: function(){
                    self.resizeIframe();
                    varsBox.toggleClass('bg-empty', varsBox.is(':empty'));
                }
            });
        },
        initSnippetPlugins: function(){
            var self = this,
                varsBox = $(self.options.variables);

            $(self.options.snippetItems).each(function(){
                $(this).click(function(){
                    // mark selected
                    $(this).addClass('active').siblings().removeClass('active');
                    var snippetId = parseInt($(this).attr('data-snippet'), 10);
                    self.loadVariables(snippetId);
                });
            });

            $('form').submit(function () {
                return !self._variablesSubmission;
            });

            varsBox.toggleClass('bg-empty', varsBox.is(':empty'));
        },
        initOpts: function(opts){
            this.options = $.extend(opts, {
                snippets: opts.variables_module + ' .snippets-list',
                snippetItems: opts.variables_module + ' .snippets-list li',
                variables: opts.variables_module + ' .variables-list'
            });
        },
        setHeaders: function () {

            function csrfSafeMethod(method) {
                // these HTTP methods do not require CSRF protection
                return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
            }

            $.ajaxSetup({
                global: true,
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type)) {
                        xhr.setRequestHeader(
                            "X-CSRFToken",
                            $('input[name="csrfmiddlewaretoken"]').val()
                        );
                    }
                },
                cache: false
            });
        },
        resizeIframe: function() {
            var insideIframe = (window.location != window.parent.location) ? true : false;
            if (!insideIframe) { return; }
            var documentHeight = Math.max($('html').outerHeight(true),
                                          $('body').outerHeight(true));
            var _jQuery = window.parent.jQuery || window.parent.$ || (window.parent.django && window.parent.django.jQuery);
            _jQuery(window.frameElement).css('height', documentHeight + 'px');
        },
        alertOnSave: function () {
            var self = this;
            $('form').submit(function () {
                if ($(self.options.snippetItems + '.selected').length > 0){
                    var answer = confirm("Changes not saved.\n" +
                        "Saving the " + self.options.plugin_name +
                        " without first saving the smart snippet will result" +
                        " in losing your changes. To prevent that, press" +
                        " 'Cancel' and save the smart snippet first.");
                    return answer;
                }
            });

        }
    };

    SnippetVariablesEditor = window.SnippetVariablesEditor || {
        init: function(requiredOpts) {
            _editor.initOpts(requiredOpts);
            _editor.initSnippetPlugins();
            _editor.setHeaders();
            _editor.resizeIframe();
            _editor.alertOnSave();
        }
    };
})(django.jQuery);
