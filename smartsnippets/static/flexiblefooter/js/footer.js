(function($){
    var FOOTER = {};

    function getDetails(){
        var inputs = $('#smartsnippetpointer_form fieldset.details .subvar, #var_logo');
        var details = {};

        inputs.each(function(){
            if($(this).attr("name") === '_logo_'){
                details["logo"] = $(this).val();
            }else{
                details[$(this).attr("name")] = $(this).val();
            }
        });

        return details;
    }

    function getLinks(){
        var cols = $('#smartsnippetpointer_form .column');
        var links = [];

        cols.each(function(){
            var column = {};

            column["header"] = {};
            $(this).find('.header input').each(function(){
                if($(this).hasClass("text")){
                    column.header["text"] = $(this).filter('.text').val();
                }
                if($(this).hasClass("url")){
                    column.header["url"] = $(this).filter('.url').val();
                }
                
            });

            column["column_links"] = [];

            $(this).find('.link').each(function(){
                column.column_links.push({
                    'text' : $(this).find('.text').val(),
                    'url' : $(this).find('.url').val()
                });
            });

            links.push(column);

        });

        return links;
    }

    function getCopyRight(){
        return $('#smartsnippetpointer_form #copyright').val();
    }

    function hideRows(){
        $('.link').hide();
        $('.link').filter(function(){
            var linkInputs = $(this).find('input').filter(function(){
                if($(this).val()){
                    return true;
                }
                return false;
            });
            if(linkInputs.length){
                return true;
            }
            return false;
        }).show();
    }

    function toggleAddLink(column){
        if(!column){
            return;
        }

        var visible = column.find('.link:visible').length;
        var total = column.find('.link').length;

        if(visible < total){
            column.find('.addlink').closest('tr').show();
        }else{
            column.find('.addlink').closest('tr').hide();
        }
    }

    function setAddLinkHanldler(){

        $('#smartsnippetpointer_form .addlink').unbind("click");
        $('#smartsnippetpointer_form .addlink').bind("click", function(){
            $(this).closest('.column').find('.link:hidden:first').show();
            toggleAddLink($(this).closest('.column'));
        });
    }

    $('form#smartsnippetpointer_form').unbind("submit");
    $(document).ready(
        function () {
            hideRows();
            setAddLinkHanldler();

            $('form#smartsnippetpointer_form .column').each(function(){
                toggleAddLink($(this));
            });

            $('form#smartsnippetpointer_form').unbind("submit");
            $('form#smartsnippetpointer_form').submit(function(){
                var footer = {};

                footer['details'] = getDetails();
                footer['links'] = getLinks();
                footer['copyright'] = getCopyRight();

                $('.snippet-varible').val(JSON.stringify(footer));

            });
        }
    );
    
}(django.jQuery));
