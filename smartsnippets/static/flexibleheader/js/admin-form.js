(function($){
    function limitChars(elems, limit, counter){
        console.log("limit")
        var keys = [8, 9, 16, 17, 18, 19, 20, 27, 33, 34, 35, 36, 37, 38, 39, 40, 45, 46, 144, 145];
        var total = limit;

        function getTotal(){
            var s = 0;
            elems.each(function(){
                s += $(this).val().length;
            });  

            return limit-s < 0 ? 0 : limit-s;  
        }

        
        
        function handler(e){
            total = getTotal();
            if( $.inArray(e.keyCode, keys) == -1) {
                if(total <= 0){
                    e.preventDefault();
                    e.stopPropagation();
                    total = 0;
                }
            }

            counter.html(total);

        }

        elems.bind({
            keydown: function(e){
                total = getTotal();
                handler(e);
              
            },
            keyup: function(e){
                if(e.target.value.length > limit){
                    e.target.value = e.target.value.substring(0, total);
                }
                total = getTotal();
                counter.html(total);
            },
            cut : handler,

        });

        counter.html(getTotal());

    }

    function saveSnippet(){
        var snippet = {};


        $('.section input').each(function(){
            snippet[$(this).attr("name").replace(/_/g, "")] = $(this).val();
        });

        $('#var_header').val(JSON.stringify(snippet));
    }

    $(document).ready(
        function () {
            limitChars($('#var_Link1_Text, #var_Link2_Text, #var_Link3_Text'), 30, $('#remaining-chars'));

            $('#var_Donate-button-text').attr("maxlength", 8);

            $('#smartsnippetpointer_form input[name="_save"]').click(function(){
                saveSnippet();
            });
        }
    );
    
}(django.jQuery || jQuery));