(function($) {
  $(document).ready(function(){

    /* Walks through each widget in the admin and initializes it */
    $("ul.jquery-tag-it-widget").each(function(){
      var field_selector = "#id_" + $(this).data("field-id");
      $(this).tagit({
        // fieldName: $(this).data("form-name"),
        singleField: true,
        allowSpaces: true,
        singleFieldDelimiter: ', ',
        singleFieldNode: $(field_selector),
        placeholderText: $(this).data("placeholder-text"),
        caseSensitive: false,
        preprocessTag: function(tag){
          if (!tag) { return ''; }
          tag = tag.trim();
          /* Remove the beginning and trailing quotes if they wrap the tag */
          if (tag.charAt(0) == '"' && tag.charAt(tag.length-1) == '"') {
            tag = tag.substring(1, tag.length-1);
          }
          return tag;
        }
      });
    });

  });
})(django.jQuery);
