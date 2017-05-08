(function($) {
  $(document).ready(function(){

    /* Walks through each widget in the admin and initializes it */
    $("ul.jquery-tag-it-widget").each(function(){
      var field_selector = "#id_" + $(this).data("field-id");
      $(this).tagit({
        singleField: true,
        allowSpaces: true,
        singleFieldDelimiter: ', ',
        singleFieldNode: $(field_selector),
        placeholderText: $(this).data("placeholder-text"),
        caseSensitive: false,
        preprocessTag: function(tag){
          /* Before the tag is added, the preprocessor removes any wrapping quotes */
          if (!tag) { return ''; }
          tag = tag.trim();
          if (tag.charAt(0) == '"' && tag.charAt(tag.length-1) == '"') {
            tag = tag.substring(1, tag.length-1);
          }
          return tag;
        }
      });
    });

  });
})(django.jQuery);
