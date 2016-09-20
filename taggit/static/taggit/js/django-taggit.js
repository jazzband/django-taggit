(function($) {
  $(document).ready(function(){

    /* Walks through each widget in the admin and initializes it */
    $("ul.jquery-tag-it-widget").each(function(){
      $(this).tagit({
        fieldName: $(this).data("form-name"),
        singleField: true,
        allowSpaces: true,
        singleFieldDelimiter: ', ',
        placeholderText: $(this).data("placeholder-text"),
        caseSensitive: false
      });
    });

  });
})(django.jQuery);
