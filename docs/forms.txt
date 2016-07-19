.. _tags-in-forms:

Tags in forms
=============

The ``TaggableManager`` will show up automatically as a field in a
``ModelForm`` or in the admin. Tags input via the form field are parsed
as follows:

* If the input doesn't contain any commas or double quotes, it is simply
  treated as a space-delimited list of tag names.

* If the input does contain either of these characters:

  * Groups of characters which appear between double quotes take
    precedence as multi-word tags (so double quoted tag names may
    contain commas). An unclosed double quote will be ignored.

  * Otherwise, if there are any unquoted commas in the input, it will
    be treated as comma-delimited. If not, it will be treated as
    space-delimited.

Examples:

====================== ================================= ================================================
Tag input string       Resulting tags                    Notes
====================== ================================= ================================================
apple ball cat         ``["apple", "ball", "cat"]``      No commas, so space delimited
apple, ball cat        ``["apple", "ball cat"]``         Comma present, so comma delimited
"apple, ball" cat dog  ``["apple, ball", "cat", "dog"]`` All commas are quoted, so space delimited
"apple, ball", cat dog ``["apple, ball", "cat dog"]``    Contains an unquoted comma, so comma delimited
apple "ball cat" dog   ``["apple", "ball cat", "dog"]``  No commas, so space delimited
"apple" "ball dog      ``["apple", "ball", "dog"]``      Unclosed double quote is ignored
====================== ================================= ================================================


``commit=False``
~~~~~~~~~~~~~~~~

If, when saving a form, you use the ``commit=False`` option you'll need to call
``save_m2m()`` on the form after you save the object, just as you would for a
form with normal many to many fields on it::

    if request.method == "POST":
        form = MyFormClass(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            # Without this next line the tags won't be saved.
            form.save_m2m()
