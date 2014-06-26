(function($){
    var FOOTER = {};

    function getDetails(){
        var inputs = $('#smartsnippetpointer_form fieldset.details .subvar');
        var details = {};

        inputs.each(function(){
            details[$(this).attr("name")] = $(this).val();
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

function showRelatedObjectLookupPopupImgField(caller, destination_id) {
    var name, href, win;

    image_field_name = destination_id;
    name = caller.id.replace(/^lookup_/, '');
    name = id_to_windowname(name);

    if (caller.href.search(/\?/) >= 0) {
        href = caller.href + '&pop=1';
    } else {
        href = caller.href + '?pop=1';
    }
    win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
    win.focus();
    //  In case the SmartSnippet has both image and merlin fields, the request to
    //  opener.dismissRelatedImageLookupPopup should go to the right function
    window.dismissRelatedImageLookupPopup = dismissRelatedImageLookupPopupImgField;

    return false;
}

dismissRelatedImageLookupPopupImgField = function (win, chosenId, chosenThumbnailUrl, chosenDescriptionTxt) {
    "use strict";

    var jxhr, jQuery = django.jQuery;

    win.close();
    jxhr = jQuery.ajax({
        url: filer_image_url,
        data: {'id': chosenId},
        success: function (data) {
            if (data.url) {
                jQuery("td.invalid_image").html('');
                jQuery('#' + image_field_name).val(data.url);
                jQuery('#' + image_field_name).next("img").attr("src",data.url);
            } else {
                jQuery("td.error_" + image_field_name).html('Please select a valid image type.');
            }
        },
        error: function (data) {
            alert('Error retrieving file information.');
        }
    });
    return jxhr;
};