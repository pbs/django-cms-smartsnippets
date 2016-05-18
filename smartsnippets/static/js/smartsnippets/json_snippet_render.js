//<![CDATA[
(function($) {
    function runOnLoad(f) {
        if (runOnLoad.loaded){
	    f();
        } else{
	    runOnLoad.funcs.push(f);
        }
    }
    runOnLoad.funcs = [];
    runOnLoad.loaded = false;
    runOnLoad.run = function() {
        if (runOnLoad.loaded) return;

        for(var i = 0; i < runOnLoad.funcs.length; i++) {
	    try {
	        runOnLoad.funcs[i]();
	    }catch(e) { }
        }
        runOnLoad.loaded = true;
        delete runOnLoad.funcs;
        delete runOnLoad.run;
    };
    if (window.addEventListener){
        window.addEventListener("load", runOnLoad.run, false);
    }else if (window.attachEvent){
        window.attachEvent("onload", runOnLoad.run);
    }else{
        window.onload = runOnLoad.run;
    }
    runOnLoad(function(){
        parent.setiframeheight($('body').height()+20, plugin_id);
    });

    $(document).ready(function(){
        $("a.add-another,a.related-lookup").each(function(i, sign){
	    var href = $(sign).attr("href");
	    if (href.substr(0,2) == ".."){
	        href = "../../" + href;
	        $(sign).attr("href", href);
	    }
        });

        var submitBtnName;

        function is_json_field(element) {
            var json_field_classes = ["merlinfield_hidden"],
                classes = element.attr('class').split(/\s+/),
                index;
            for (index=0; index<json_field_classes.length; index++) {
                if (classes.indexOf(json_field_classes[index]) !== -1) {
                    return true;
                }
            }
            return false;
        }

        SnippetWidgetRegistry.initializeVariables();
        $(form_id).find(':submit').click(function(){
            submitBtnName  = $(this).attr('name');
        });
        $(form_id).submit(function(){
            if (!SnippetWidgetRegistry.allValid()) {
                return false;
            }
            var data={};
            $('input, textarea, select').each(function(){
                var id=$(this).attr('id'),
                    value=this.value,
                    classes=[];
                if (id && value && id.startsWith('var_')) {
                    if (is_json_field($(this))) {
                        value = JSON.parse(value);
                    }
                    data[id.substring(4)] = value;
                }
            });
            console.log("This JSON must be saved somewhere:", JSON.stringify(data));
            return false;
        });

        $('#id_snippet').change(function(){
            var selected_snippet = $('#id_snippet').val();
            var url = window.location.href;
            url += (url.indexOf('?') !== -1 ? '&':'?') + "snippet=" + selected_snippet;
            window.location = url;
        });

    });

    $(document).ready(function(){
        if (window.hasAceTheme == true) {
            $('.plugin-help-tooltip').remove();
        }
        else {
            $('.smartsnippet-description').remove();
        }
    });
})(jQuery || django.jQuery);
//]]>
