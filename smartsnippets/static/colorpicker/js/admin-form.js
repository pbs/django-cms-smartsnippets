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

    function toggleView(view){
        if(!view){
            $('#color-picker-views').hide();
            resizeIframe()
            return;
        }

        if(view === true){
            $('#color-picker-views').removeAttr("style");
            $('.view').hide();
            $('#step_1').show();
            resizeIframe()
            return;
        }

        $('.view').hide();
        view.show();
        resizeIframe()

    }

    function setDefaultView(theme){
        if(theme != 'explorer'){
            toggleView(true);
            $('#smartsnippetpointer_form table tr:not(#color-picker-views)').hide();
            $('.plugin-submit-row input[name="_save"]').val("Save and Apply New Theme to My Site").attr("disabled", true);
        }else{
            toggleView(false);
            $('#smartsnippetpointer_form table tr:not(#color-picker-views)').show();
            $('.plugin-submit-row input[name="_save"]').val("Save").removeAttr("disabled");
        }
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
        scheme[1] = tinycolor.lighten(result[1], 88);
        scheme[2] = tinycolor.darken(result[2], 10);
        scheme[3] = tinycolor.lighten(result[3], 25);
        scheme[4] = result[4];
        if(output){
            output.each(function(iter){
                $(this).css('background-color', scheme[iter].toHexString());
                $(this).parent().find('.title.hex').html(scheme[iter].toHexString());
            });
        }

        

    }

    function initStep_2_a(){
        var defaultColor = '#0000ff';

        $('#colorpickerHolder').ColorPicker({
            color: defaultColor,
            flat: true,
            onChange: function (hsb, hex, rgb) {
                generateColorScheme(hex, $('#step_2_a .colors-placeholder .output'));
                // $('#colorSelector div').css('backgroundColor', '#' + hex);
            }
        });

        generateColorScheme(defaultColor, $('#step_2_a .colors-placeholder .output'));

        $('.plugin-submit-row input[name="_save"]').val("Save and Apply New Theme to My Site").removeAttr("disabled");
    }

    function initStep_2_b(){
        // $('#step_2_b .scheme-container').each(function(){
        //     var hex = $(this).find('input[type="radio"]').val();
        //     generateColorScheme(hex, $(this).find('.output'));
        // });
        $('.plugin-submit-row input[name="_save"]').val("Save and Apply New Theme to My Site").removeAttr("disabled");
    }

    function handleSubmitButton(){
        var form = $('#smartsnippetpointer_form');

        var handleSubmit = function(handler){
            if(handler){
                form.submit(handler);
            }else{
                form.submit(function(){
                    return false;
                });
            }
        };

        form.find('input[type="submit"]:not(input[name="_cancel"]), .footer-view .cancel').unbind("click");
        form.find('input[type="submit"]:not(input[name="_cancel"]), .footer-view .cancel').click(function(){
            
            if($(this).attr('name') == "next"){
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
            }

            if($(this).attr('name') == "reset"){
                toggleView($('#step_1'));
                handleSubmit(false);
            }

            if($(this).attr('data-name') == "cancel"){
                $('#var_theme option').filter(function() { 
                    return ($(this).text() == 'explorer');
                }).attr('selected', true);
                setDefaultView($('#var_theme').val());
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
