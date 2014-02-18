(function($){
    function resizeIframe(){
        var bodyH = $('body').height();
        try{
            var parentJQuery = window.parent.jQuery || window.parent.django.jQuery;
        }catch(e){
        }

        if(typeof parentJQuery != undefined && parentJQuery){
            parentJQuery('iframe').css("height", bodyH);
        }
        
    }

    function getPreviewHTML(){
        var HTML = "";
        var elems = [{
                "tag": "div",
                "attr": "id='top-stripe' class='main_color'",
            },{
                "tag": "div",
                "attr": "id='top-theree-links' ",
                "text": "<a>Log In</a> | <a>Shop</a> | <a>Donate</a>"
            },{
                "tag": "div",
                "attr": "id='menu-btn' class='main_color'",
                "text": "HOME"
            },{
                "tag": "div",
                "attr": "id='menu-stripe' class='main_color'"
            },{
                "tag" : "span",
                "attr": "class='search button_color'"
            },{
                "tag": "div",
                "attr" : "id='right_rail_add' class='light_accent'",
            },{
                "tag": "a",
                "attr" : "id='pledge' href='javascript:void(0)'",
                "text" : "Pledge your support today &gt;"
            },{
                "tag": "div",
                "attr": "id='module-header' class='light_accent'",
            },{
                "tag": "a",
                "attr": "id='module-text1' href='javascript:void(0)'",
                "text":"linked text"
            },{
                "tag": "a",
                "attr": "id='module-text2' href='javascript:void(0)'",
                "text":"Linked Text"
            },{
                "tag": "div",
                "attr": "id='footer-stripe' class='main_color'",
            },{
                "tag": "div",
                "attr": "id='copyright' class='main_color'",
            }];

        var scheme = window.opener.colorScheme;

        HTML += "<style>";
            for(var i in scheme){
                if(scheme.hasOwnProperty(i)){
                    if(i != 'background' && i !='apply_overlay'){
                        HTML += '.'+i+'{ background-color: '+scheme[i]+';}';
                    }
                    if(i == 'background'){
                        HTML += 'body{background-color:'+scheme[i]+'}';
                    }
                    if(i == 'apply_overlay'){
                        if(scheme[i].toLowerCase() != 'true'){
                            HTML += 'body{background-image:none}';
                        }else{
                            $('body').addClass('explorer passport '+scheme.id);
                        }
                    }


                    HTML += '#preview a, #preview a:hover{color:'+scheme.darker_accent+'}';
                }
            }
        HTML += "</style>";

        HTML += '<div id="preview">';
            for(var i=0; i<elems.length; i++){
                if(elems[i].tag){
                    HTML += '<'+elems[i].tag+' '+(elems[i].attr ? elems[i].attr : "")+'>'+(elems[i].text ? elems[i].text : "")+'</'+elems[i].tag+'>';
                }
            }
        HTML += '</div>';

        return HTML;
    }

    function toggleView(view){

        if(!view){
            $('#color-picker-views').hide();
            resizeIframe();
            return;
        }

        if(view === true){
            $('#color-picker-views').removeAttr("style");
            $('.view').hide();
            $('#step_1').show();
            resizeIframe();
            return;
        }

        $('.view').hide();
        view.show();
        resizeIframe();

    }

    function setDefaultView(theme){

        $('#container').css("visibility", "visible");

        if(theme == 'passport'){
            toggleView(true);
            $('#smartsnippetpointer_form table tr:not(#color-picker-views)').hide();
            $('.plugin-submit-row input[name="_save"]').val("Save and Apply New Theme to My Site").attr("disabled", true);
        }else{
            toggleView(false);
            $('#smartsnippetpointer_form table tr:not(#color-picker-views)').show();
            $('.plugin-submit-row input[name="_save"]').val("Save").removeAttr("disabled");
        }

        //used when loading same page in new window to view the preview
        try{
            if(window.location.href.split("?")[1].indexOf("preview") != -1){
                $('#container').css({
                    "visibility": "hidden", 
                    "height":"0px"});
                $('#container').hide();
                $('#color-picker-css').remove()
                $('body').append(getPreviewHTML());
            }
        }catch(e){}
    }

    function generateColorScheme(hex, output){
        if(!hex){
            return false;
        }

        var color = tinycolor(hex);  
        var result = tinycolor.monochromatic(color, 5).splice(1);

        result.sort(function(a, b){
            a = a.toHsl();
            b = b.toHsl();
            return a.l - b.l;
            
        });
        result = [color].concat(result);
        scheme = [];
        scheme[0] = color;
        scheme[1] = tinycolor.lighten(result[1], 90);
        scheme[2] = tinycolor.darken(result[2], 10);
        scheme[3] = tinycolor.lighten(result[3], 25);
        scheme[4] = result[4];
        if(output){
            output.each(function(iter){
                $(this).css('background-color', scheme[iter].toHexString());
                $(this).parent().find('.title.hex').html(scheme[iter].toHexString());
            });
        }

        $('#color-picker-views #step_2_a #background option:first').attr("data-val", scheme[1].toHexString());
    }

    function getFormScheme(){
        var profile = $('#color-picker-views #step_1 input[name="profile"]:checked').val();
        var scheme = {};
        var hexElems = null;

        if(profile == "custom"){
            hexElems = $('#color-picker-views #step_2_a .title.hex');
            scheme.apply_overlay = "";
            scheme.background = $('#color-picker-views #step_2_a #background option:selected').attr("data-val");
        }

        if(profile == "preselected"){
            var radioBtn = $('#color-picker-views #step_2_b input[name="scheme"]:checked');
            hexElems = radioBtn.next('.scheme').find('.title.hex');
            scheme.apply_overlay = $('#color-picker-views #step_2_b input[name="apply-overlay"]').is(":checked") ? "true" : "";
            scheme.id = radioBtn.next('.scheme').attr("data-name")
        }

        hexElems.each(function(){
            var key = $(this).attr("data-name");
            var val = $(this).text();
            if(!scheme[key]){
                scheme[key] = val;
            }
        });

        return scheme;
    }

    function initStep_2_a(){
        $('#smartsnippetpointer_form').unbind("submit");
        var defaultColor =  '#0000ff';
        try{
            var scheme_color = JSON.parse($('.snippet-varible').val()).main_color;
        }catch(e){}

        $('#colorpickerHolder').ColorPicker({
            color: (scheme_color || defaultColor),
            flat: true,
            onChange: function (hsb, hex, rgb) {
                generateColorScheme(hex, $('#step_2_a .colors-placeholder .output'));
                // $('#colorSelector div').css('backgroundColor', '#' + hex);
            }
        });

        generateColorScheme((scheme_color || defaultColor), $('#step_2_a .colors-placeholder .output'));

        $('.plugin-submit-row input[name="_save"]').val("Save and Apply New Theme to My Site").removeAttr("disabled");
    }

    function initStep_2_b(){
        $('.plugin-submit-row input[name="_save"]').val("Save and Apply New Theme to My Site").removeAttr("disabled");
        try{
            var json = JSON.parse($('.snippet-varible').val());
            $('#step_2_b .title.hex[data-name="main_color"]').each(function(){
                if(json.main_color == $(this).text()){
                    $(this).closest('.scheme-container').find("input[name='scheme']").attr("checked", true);
                }
            });
            if(json.apply_overlay.toLowerCase() == "true"){
                $('#step_2_b input[name="apply-overlay"]').attr("checked", true);
            }
        }catch(e){}
    }

    function handleSubmitButton(){
        var form = $('#smartsnippetpointer_form');

        var handleSubmit = function(handler){
            
            if(handler){
                form.bind("submit",handler);
            }else{
                form.bind("submit",function(){
                    return false;
                });
            }
        };

        form.find('input[type="submit"], .footer-view .cancel').unbind("click");
        form.find('input[type="submit"], .footer-view .cancel').click(function(){
            //"next" button is pressed
            if($(this).attr('name') == "next"){
                form.unbind("submit")
                var radioVal = form.find('input[name="profile"]:checked', form).val();

                if(radioVal == "custom"){
                    toggleView($('#step_2_a'));
                    handleSubmit(false);
                    initStep_2_a();
                }else{
                    toggleView($('#step_2_b'));
                    handleSubmit(false);
                    initStep_2_b();
                }

                return false
            }

            //"back to step one" button is pressed
            if($(this).attr('name') == "reset"){
                toggleView($('#step_1'));
                handleSubmit(false);
                return
            }

            //"concel" button is pressed
            if($(this).attr('name') == "_cancel"){
                form.unbind("submit");
                return
            }

            //"undo" button is pressed
            if($(this).attr('data-name') == "cancel"){
                $('#var_theme option').filter(function() { 
                    return ($(this).text() == 'explorer');
                }).attr('selected', true);
                setDefaultView($('#var_theme').val());
            }

            //"preview scheme" button is pressed
            if($(this).attr('name') == "preview"){
                var page = $('#step_1 input[name="profile"]:checked').val();
                
                win = window.open(window.location.href + "?preview="+page, "preview", 'height=600,width=1034,resizable=no,scrollbars=no');

                win.focus();
                window.colorScheme = getFormScheme();
                handleSubmit(false);
            }

            //"save and apply new theme" button is pressed
            if($(this).attr('name') == "_save"){
                form.unbind("submit")
                handleSubmit(function(){
                    var scheme = getFormScheme();
                    $('.snippet-varible').val(JSON.stringify(scheme));
                });
                form.submit();
                return true;
            }
        });
    }

    $(document).ready(
        function () {
            $('body').bind("change", function(){
                resizeIframe();
            });

            handleSubmitButton();

            $('#var_theme').change(function(){
                setDefaultView($(this).val());
            });

            $('#step_2_b .scheme-container .scheme, .label').click(function(){
                $(this).prev('input[type="radio"]').attr("checked", true);
                if($(this).prev('input[type="checkbox"]').is(":checked")){
                    $(this).prev('input[type="checkbox"]').attr("checked", false);
                }else{
                    $(this).prev('input[type="checkbox"]').attr("checked", true);
                }
            });

            setDefaultView($('#var_theme').val());
            
        }
    );
    
}(django.jQuery));
