(function ($) {
    $(document).ready(function () {
        $("div.form-row.field-size_set").hide();
        $("div.form-row.field-widget").each(function (index) {
            var parent = this;
            $(this).find("select").change(function(ev) {
                if (ev.target.value.indexOf("ImageField") >= 0) {
                    $(parent).next().show();
                } else {
                    $(parent).next().hide();
                }
            });
            if ($(this).find("select option:selected").val().indexOf('ImageField') >= 0) {
                $(this).next().show();
            }
        });
    });

})(django.jQuery);