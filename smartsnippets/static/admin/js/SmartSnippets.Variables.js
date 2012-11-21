(function ($) {

    var LayoutParser = {
        emptyContainer:function (container) {
            container.children('.inline-related ').each(function (i, item) {
                if (!$(item).hasClass('empty-form'))
                    $(item).remove();
            });
        },

        getContainer:function (variablesHolderType) {
            var cx = null;
            $('.inline-group').each(function (i, item) {
                if (variablesHolderType == 'standard') {
                    if ($(item).children('h2')[0].innerText.toLowerCase() == 'standard variables') {
                        cx = $(item);
                        return;
                    }

                } else if (variablesHolderType == 'select') {
                    if ($(item).children('h2')[0].innerText.toLowerCase() == 'drop down variables') {
                        cx = $(item);
                        return;
                    }
                }
            });

            return cx;
        },

        clickAddNewFieldStd:function (container) {
            var addNewFieldBtn = $(container).children('div.add-row').find('a');
            addNewFieldBtn.trigger('click');

            var addedField = $(container).children('.inline-related').last().prev();

            return addedField;
        },

        clickAddNewFieldSelect:function (container) {
            var addNewFieldBtn = $(container).children('div.add-row').find('a');
            addNewFieldBtn.trigger('click');

            var addedField = $(container).children('.inline-related').last().prev();

            return addedField;
        },

        addStdVar:function (varNameObj, container) {
            var fieldCx = this.clickAddNewFieldStd(container);
            $(fieldCx).find('input.vTextField')[0].value = varNameObj.varname;
            $(fieldCx).find('select')[0].value = varNameObj.type;
        },

        addSelectVar:function (varNameObj, container) {
            var fieldCx = this.clickAddNewFieldSelect(container);
            $(fieldCx).find('div.field-name').find('input.vTextField')[0].value = varNameObj.varname;
            $(fieldCx).find('div.field-choices').find('input.vTextField')[0].value = varNameObj.values;
        }
    };

    $(document).ready(function () {
        $('#id_template_code').bind('paste', function (e) {
            var el = $(this);
            setTimeout(function () {
                var text = $(el).val();

                var regex = /<!-- SmartSnippets Variables([^>]*)-->/gi;
                var variablesSnippet = regex.exec(text);
                if (variablesSnippet) {
                    var lines = variablesSnippet[1].split('\n'); //split the input in multiple lines
                    var varNames = []; //hold the var names here

                    $.each(lines, function (index, line) {
                        if (line.replace(/^\s+|\s+$/, '').length > 0) {
                            var vObj = {};
                            var vDeclarationArr = line.split('=');
                            vObj.varname = vDeclarationArr[0].replace(/^\s+|\s+$/, '');

                            var type = vDeclarationArr[1].replace(/^\s+|\s+$/, '');
                            if (type.toLowerCase().indexOf('select') != -1) {
                                var tmp = type.split('|');
                                vObj.type = tmp[0].replace(/^\s+|\s+$/, '');
                                vObj.values = vDeclarationArr[2] ? vDeclarationArr[2].replace(/^\s+|\s+$/, '') : '';
                            } else {
                                vObj.type = vDeclarationArr[1].replace(/^\s+|\s+$/, '');
                            }

                            varNames.push(vObj);
                        }
                    });

                    if (varNames.length > 0) { //don't do any mumbo jumbo if we have no varnames

                        var stdContainer = LayoutParser.getContainer('standard');
                        var selectContainer = LayoutParser.getContainer('select');

                        LayoutParser.emptyContainer(stdContainer);
                        LayoutParser.emptyContainer(selectContainer);

                        $.each(varNames, function (i, vObj) {

                            if (vObj.type.toLowerCase() != 'select') {
                                LayoutParser.addStdVar(vObj, stdContainer);
                            } else {
                                LayoutParser.addSelectVar(vObj, selectContainer);
                            }

                        });
                    }
                }
            }, 100);
        });
    });

})(django.jQuery);
