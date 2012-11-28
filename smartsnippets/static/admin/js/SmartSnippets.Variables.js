(function ($) {

    /**
     * This object provides helper functions for parsing a pasted smart snippet's code and auto populating the variable
     * fields needed by that smart snippet.
     * @type {Object}
     */
    var LayoutParser = {

        /**
         * Clear all added variables from a container
         * @param jQuery container
         */
        emptyContainer:function (container) {
            container.children('.inline-related ').each(function (i, item) {
                if (!$(item).hasClass('empty-form'))
                    $(item).remove();
            });
        },

        /**
         * Gets the standard variables container or the drop down one
         * @param String variablesHolderType
         * @return {*\jQuery}
         */
        getContainer:function (variablesHolderType) {
            var cx = null;
            $('.inline-group').each(function (i, item) {
                if (variablesHolderType == 'standard') {

                    var header = $(item).children('h2').get(0);
                    if ($(header).text().toLowerCase() == 'standard variables') {
                        cx = $(item);
                        return;
                    }

                } else if (variablesHolderType == 'select') {

                    var header = $(item).children('h2').get(0);

                    if ($(header).text().toLowerCase() == 'drop down variables') {
                        cx = $(item);
                        return;
                    }
                }
            });

            return cx;
        },

        /**
         * Find the "Add another Standard Variable" button and trigger a click event on it. Returns the div container
         * holding form fields
         * @param container
         * @return {*|jQuery}
         */
        clickAddNewFieldStd:function (container) {

            //count the number of already inserted vars here
            //subtract 1 for the empty one present by default
            var presentFieldsCount = container.children('.inline-related').length - 1;

            var addNewFieldBtn = $(container).children('div.add-row').find('a');
            addNewFieldBtn.trigger('click');

            var addedField = $(container).children('.inline-related').last().prev();

            var textField = addedField.find('input.vTextField');
            $(textField).attr('id', 'id_variables-' + presentFieldsCount + '-name');
            $(textField).attr('name', 'variables-' + presentFieldsCount +'-name');

            var select = addedField.find('div.field-widget').find('select');
            $(select).attr('id', 'id_variables-' + presentFieldsCount + '-widget');
            $(select).attr('name', 'variables-' + presentFieldsCount + '-widget');

            return addedField;
        },

        /**
         * Find the "Add another Drop Down Variable" button and trigger a click event on it. Returns the div container
         * holding form fields. There is really no difference at the moment between this and the clickAddNewFieldStd.
         * The only reason for them to be separate is for expressiveness and future extensions.
         * @param container
         * @return {*|jQuery}
         */
        clickAddNewFieldSelect:function (container) {
            var addNewFieldBtn = $(container).children('div.add-row').find('a');
            addNewFieldBtn.trigger('click');

            var addedField = $(container).children('.inline-related').last().prev();
            var inputFields = addedField.children('.vTextField');

            var presentFieldsCount = container.children('.inline-related').length;

            $(inputFields[0]).attr('id', 'id_variables-2-' + presentFieldsCount +'-name');
            $(inputFields[0]).attr('name', 'variables-2-' + presentFieldsCount + '-name');

            $(inputFields[1]).attr('id', 'id_variables-2-' + presentFieldsCount + '-choices');
            $(inputFields[1]).attr('name', 'variables-2-' + presentFieldsCount + '-choices');

            return addedField;
        },

        /**
         * Add a new standard variable in the container
         * varNameObj = {varname: 'name', type: 'type'}
         * @param varNameObj
         * @param container
         */
        addStdVar:function (varNameObj, container) {
            var fieldCx = this.clickAddNewFieldStd(container);
            $(fieldCx).find('input.vTextField')[0].value = varNameObj.varname;
            $(fieldCx).find('select')[0].value = varNameObj.type;
        },

        /**
         * Add a new drop down variable in the container
         * varNameObj = {varname: 'name', type: 'type', values: 'value1,value2,value3'}
         * @param varNameObj
         * @param container
         */

        addSelectVar:function (varNameObj, container) {
            var fieldCx = this.clickAddNewFieldSelect(container);
            $(fieldCx).find('div.field-name').find('input.vTextField')[0].value = varNameObj.varname;
            $(fieldCx).find('div.field-choices').find('input.vTextField')[0].value = varNameObj.values;
        },

        /**
         * The following code will try to match everything that's within an html comment tag. It should look like this
         *
         * <!-- SmartSnippets Variables
         * varname=type
         * -->
         *
         * Where type could be anything from TextField, TextAreaField, MerlinField or ImageField
         * Each variable is declared on a new line.
         */
        extractVarnames:function (text) {
            var regex = /<!-- SmartSnippets Variables([^>]*)-->/gi;
            var variablesSnippet = regex.exec(text);
            var varNames = []; //hold the var names here

            if (variablesSnippet) {
                var lines = variablesSnippet[1].split('\n'); //split the input in multiple lines

                $.each(lines, function (index, line) {
                    if ($.trim(line).length > 0) {
                        var vObj = {};
                        var vDeclarationArr = line.split('=');
                        vObj.varname = $.trim(vDeclarationArr[0]);

                        var type = $.trim(vDeclarationArr[1]);
                        if (type.toLowerCase().indexOf('select') != -1) {
                            var tmp = type.split('|');
                            vObj.type = $.trim(tmp[0]);
                            vObj.values = vDeclarationArr[2] ? $.trim(vDeclarationArr[2]) : '';
                        } else {
                            vObj.type = $.trim(vDeclarationArr[1]);
                        }

                        varNames.push(vObj);
                    }
                });
            }
            return varNames;
        },

        /**
         * Given an array of objects with the following structure {varname: 'name', type: 'type', values: 'value1,
         * value2,value3'} or varNameObj = {varname: 'name', type: 'type'} this function fill parse the array.
         *
         * @param varNamesArr
         */
        populate:function (varNamesArr) {
            var self = this;
            if (varNamesArr.length > 0) { //don't do any mumbo jumbo if we have no varnames

                var stdContainer = self.getContainer('standard');
                var selectContainer = self.getContainer('select');

                self.emptyContainer(stdContainer);
                self.emptyContainer(selectContainer);

                $.each(varNamesArr, function (i, vObj) {

                    if (vObj.type.toLowerCase() != 'select') {
                        self.addStdVar(vObj, stdContainer);
                    } else {
                        self.addSelectVar(vObj, selectContainer);
                    }
                });
            }
        }
    };


    $(document).ready(function () {
        var textArea = $('#id_template_code');

        textArea.bind('paste', function (e) {
            var el = $(this);

            if ($.trim($(el).val()).length == 0) {//only when the area is empty
                //use a setTimeout to capture pasted text
                setTimeout(function () {
                    var text = $(el).val();
                    var varNames = LayoutParser.extractVarnames(text);
                    LayoutParser.populate(varNames);
                }, 100);
            }
        });
    });

})(django.jQuery);
