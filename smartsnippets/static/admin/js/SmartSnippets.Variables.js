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

        getExistingStandardVariables:function (container) {
            var fieldRows = container.children('.dynamic-variables');
            var existingVars = new Array();

            fieldRows.each(function (i, row) {
                var textField = $(row).find('.vTextField');
                var typeField = $(row).find('select');
                var name = textField.val();
                var type = typeField.val();

                var typeDocId = typeField.attr('id');
                var obj = {name:name, type:type, typeDocId:typeDocId};
                existingVars.push(obj);
            });

            return existingVars;
        },

        getExistingSelectVariables:function (container) {
            var fieldRows = container.children('.dynamic-variables-2');
            var existingVars = new Array();

            fieldRows.each(function (i, row) {
                var name = $(row).find('.field-name').find('.vTextField').val();
                var nameDocId = $(row).find('.field-name').find('.vTextField').attr('id');

                var values = $(row).find('.field-choices').find('.vTextField').val();
                var valuesDocId = $(row).find('.field-choices').find('.vTextField').attr('id');

                var obj = {name:name, values:values, valuesDocId:valuesDocId};

                existingVars.push(obj);
            });

            return existingVars;
        },


        groupExistingVars:function (existingVars, newVars, variablesType) {
            var similarVars = [];
            var updateVars = [];
            var toBeDeletedVars = [];

            var similarFieldToCheck = (variablesType && variablesType.toLowerCase() == 'select' ? 'values' : 'type');

            for (var i = 0; i < existingVars.length; i++) {
                var toBeUpdated = false;
                var updatedFieldValue = undefined;
                var isSimilar = false;
                for (var j = 0; j < newVars.length; j++) {
                    if (existingVars[i].name == newVars[j].varname && existingVars[i][similarFieldToCheck] == newVars[j][similarFieldToCheck]) {
                        isSimilar = true;
                        break;
                    } else if (existingVars[i].name == newVars[j].varname && existingVars[i][similarFieldToCheck] != newVars[j][similarFieldToCheck]) {
                        toBeUpdated = true;
                        updatedFieldValue = newVars[j][similarFieldToCheck];
                        break;
                    }
                }

                if (toBeUpdated) {
                    existingVars[i].updateWithValue = updatedFieldValue;
                    updateVars.push(existingVars[i]);
                } else if (isSimilar) {
                    similarVars.push(existingVars[i]);
                } else if (!toBeUpdated && !isSimilar) {
                    toBeDeletedVars.push(existingVars[i]);
                }
            }

            return {
                similarVars:similarVars,
                toUpdateVars:updateVars,
                deleteVars:toBeDeletedVars
            };
        },

        findByVarName:function (arr, vName) {
            var found = false;
            $.each(arr, function (i, item) {
                if (item.name == vName) {
                    found = item;
                    return;
                }
            });

            return found;
        },

        markForDeletion:function (container, deletedVars) {
            var rows = container.children('.inline-related');

            var self = this;
            $.each(rows, function (i, row) {
                var varName = $(row).find('.field-name').find('.vTextField').val();
                var isFoundVar = self.findByVarName(deletedVars, varName);

                if (isFoundVar) {
                    var deleteBtn = $(row).find('a.inline-deletelink');
                    if(deleteBtn.get(0)) {
                        //most likely variable was added from a previous paste or by the user so trigger the deletion here
                        deleteBtn.trigger('click');
                    } else {
                        var deleteCheckbox = $(row).find('.delete').find('input[type=checkbox]');
                        deleteCheckbox.attr('checked', 'checked');
                    }
                }
            });
        },

        updateVars:function (container, updatedVars, varsType) {
            var rows = container.children('.inline-related');

            var objFieldToUpdate = (varsType.toLowerCase() == 'select' ? 'valuesDocId' : 'typeDocId');

            var self = this;
            $.each(rows, function (i, row) {
                var varName = $(row).find('.field-name').find('.vTextField').val();
                var isFoundVar = self.findByVarName(updatedVars, varName);

                if (isFoundVar) {
                    $('#'+ isFoundVar[objFieldToUpdate]).val(isFoundVar.updateWithValue)
                }
            });
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

            addedField.attr('id', 'variables-' + presentFieldsCount);

            var textField = addedField.find('input.vTextField');
            $(textField).attr('id', 'id_variables-' + presentFieldsCount + '-name');
            $(textField).attr('name', 'variables-' + presentFieldsCount + '-name');

            var textLabel = addedField.find('div.field-name').find('label');
            $(textLabel).attr('for', 'id_variables-' + presentFieldsCount + '-name');

            var select = addedField.find('div.field-widget').find('select');
            $(select).attr('id', 'id_variables-' + presentFieldsCount + '-widget');
            $(select).attr('name', 'variables-' + presentFieldsCount + '-widget');

            var selectLabel = addedField.find('div.field-widget').find('label');
            $(selectLabel).attr('for', 'id_variables-' + presentFieldsCount + '-widget')

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

            $(inputFields[0]).attr('id', 'id_variables-2-' + presentFieldsCount + '-name');
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
            $(fieldCx).find('input.vTextField').val(varNameObj.varname);
            $(fieldCx).find('select').val(varNameObj.type);
        },

        /**
         * Add a new drop down variable in the container
         * varNameObj = {varname: 'name', type: 'type', values: 'value1,value2,value3'}
         * @param varNameObj
         * @param container
         */

        addSelectVar:function (varNameObj, container) {
            var fieldCx = this.clickAddNewFieldSelect(container);
            $(fieldCx).find('div.field-name').find('input.vTextField').val(varNameObj.varname);
            $(fieldCx).find('div.field-choices').find('input.vTextField').val(varNameObj.values);
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

        groupNewVars:function (varsArr) {
            var returnObj = {};
            returnObj.standard = new Array();
            returnObj.select = new Array();

            $.each(varsArr, function (i, variable) {
                if (variable.type.toLowerCase() == 'select') {
                    returnObj.select.push(variable);
                } else {
                    returnObj.standard.push(variable);
                }
            });

            return returnObj;
        },

        getOnlyToAddVars: function(groupedVars, newVars) {
            var onlyToAdd = new Array();
            for (var i = 0; i < newVars.length; i++) {
                var notInUpdates = true;
                var notInSimilar = true;

                for(var j = 0; j < groupedVars.similarVars.length; j++) {
                    if(newVars[i].varname == groupedVars.similarVars[j].name) {
                        notInSimilar = false;
                    }
                }

                for(var k = 0; k < groupedVars.toUpdateVars.length; k++) {
                    if(newVars[i].varname == groupedVars.toUpdateVars[k].name) {
                        notInUpdates = false;
                    }
                }

                if(notInSimilar && notInUpdates) {
                    onlyToAdd.push(newVars[i]);
                }
            }

            return onlyToAdd;
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

                var groupedNewVars = self.groupNewVars(varNamesArr);

                var stdContainer = self.getContainer('standard');
                var selectContainer = self.getContainer('select');

                var existingStdVars = self.getExistingStandardVariables(stdContainer);
                var existingSelectVars = self.getExistingSelectVariables(selectContainer);

                var groupedExistingStdVars = self.groupExistingVars(existingStdVars, groupedNewVars.standard, 'standard');

                if (existingStdVars.length > 0) {
                    self.markForDeletion(stdContainer, groupedExistingStdVars.deleteVars);
                    self.updateVars(stdContainer, groupedExistingStdVars.toUpdateVars, 'standard');
                }

                var groupedExistingSelectVars = self.groupExistingVars(existingSelectVars, groupedNewVars.select, 'select');
                if(existingSelectVars.length > 0) {

                    self.markForDeletion(selectContainer, groupedExistingSelectVars.deleteVars);
                    self.updateVars(selectContainer, groupedExistingSelectVars.toUpdateVars, 'select');
                }

                var onlyToAddStdVars = self.getOnlyToAddVars(groupedExistingStdVars, groupedNewVars.standard);
                var onlyToAddSelectVars = self.getOnlyToAddVars(groupedExistingSelectVars, groupedNewVars.select);


                $.each(onlyToAddStdVars, function(i, vObj) {
                    self.addStdVar(vObj, stdContainer);
                });

                $.each(onlyToAddSelectVars, function(i, vObj) {
                    self.addSelectVar(vObj, selectContainer);
                });
            }
        }
    };

    $.updateSnippetVars = function(el){

        //use a setTimeout to capture pasted text
        setTimeout(function () {

            var checkboxes = django.jQuery('.delete input[type=checkbox]');
            django.jQuery.each(checkboxes, function(i, box) {
                django.jQuery(this).attr('checked', false);
            });

            var text = django.jQuery(el).val();
            var varNames = LayoutParser.extractVarnames(text);
            LayoutParser.populate(varNames);
        }, 100);
    };


    $(document).ready(function () {
        var textArea = $('#id_template_code');

        textArea.bind('paste', function (e) {
            var el = $(this);

//            if ($.trim($(el).val()).length == 0) {//only when the area is empty
                //use a setTimeout to capture pasted text
                $.updateSnippetVars(el);
//            }
        });
    });

})(django.jQuery);
