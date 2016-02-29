django-cms-smartsnippets
========================

``smartsnippets`` is a `django-cms`_ plugin similar to the builtin `snippet`_
plugin but instead of allowing only plain HTML you can use any valid
Django template syntax inside and also
you can configure certain variables in template snippet to be filled
once the smartsnippet is added to a placeholder on a page.
This is much more flexible than the standard ``snippet`` if you want to parametrize
and reuse your static snippets.

An important feature of smartsnippets is manual specification of
variables and variable types when adding an html snippet.

Smart snippet ships a set of basic variable Field types with the app:
  TextField, TextAreaField, DropDownField.

This module also provides a registration manager for field types
  so that third party apps can hook in with custom editing fields and user admin behavior.

Demo
=======
The demo is created using resouces from the `django-cms demo`_.
To try out the demo application:

1. Checkout code:

.. code::
   git clone git@github.com:pbs/django-cms-smartsnippets.git
   git checkout master_contrib

2. Setup:

.. code::
   mkvirtualenv ss_demo; source ss_demo/bin/activate
   pip install -e ./django-cms-smartsnippets

3. Start server:

.. code::
   cd django-cms-smartnippets/demo
   ./manage.py runserver


Example
=======

Create a simple smartsnippet using the `Twitter profile example`_::

    1. Add the template code(of the path to the template file):
    <script src="http://widgets.twimg.com/j/2/widget.js"></script>
    <script>
    new TWTR.Widget({
      version: 2,
      type: 'profile',
      rpp: 4,
      interval: 30000,
      width: 250,
      height: 300,
      theme: {
        shell: {
          background: '#333333',
          color: '#ffffff'
        },
        tweets: {
          background: '{{ background }}',
          color: '#ffffff',
          links: '#4aed05'
        }
      },
      features: {
        scrollbar: false,
        loop: false,
        live: false,
        behavior: 'all'
      }
    }).render().setUser('{{ twitter_username }}').start();
    </script>

    Note the ``{{ background }}`` and ``{{ twitter_username }}`` variable used as standard Django variables.

    2. Configure background and twitter_username variables:
        a. Variable name: twitter_username
           Variable widget: TextField(because the twitter username is a simple and relatively short text)
        b. Variable name: background
           Variable widget: DropDownField
           Variable choices: #000000, #eeeeee, #cecece
    3. When adding the smartsnippet in a page, the form will provide:
        a. an input text field where you can set a value of twitter_username
        b. a select html tag having as options the list of choices (#000000, #eeeeee, #cecece)
           added when the background variable was configured.


Settings
========

Terms:

SS = Smart Snippet
Chosen Snippets List = Can be seen by accessing http://localhost:8000/admin/sites/site/40/,
                       where 40 is the id of a particular site, can be any valid id
		       It represents the list with selected SS for the current site
		       (the right one).
SS List = Can be seen by following: http://localhost:8000/admin/smartsnippets/smartsnippet/
SS Plugin drop down = This is the drop down from SS plugin which allows SSs to
                      be selected for the current page.


There are three configuration variables available:

* ``SMARTSNIPPETS_INCLUDE_ORPHAN`` a boolean flag that defaults to
  ``True``. If this option is enabled, selecting a site in the
  smartsnippet creation form is optional. If a smartsnippet doesn't
  belong to any site it will behave as global and will be available
  in all sites. If set to ``False`` the user will be forced to link
  the smartsnipptes that he creates to at least one site.

  A SS can become orphan if all its sites have been deleted. This
  setting controls if orphan SSs can be displayed in SS List
  or to be available for SS Plugin drop down.

* ``SMARTSNIPPETS_RESTRICT_USER`` a boolean flag that defaults to
  ``False``. This flag, if set, will limit the smartsnippets that
  a user can access based on his relation to sites trough the global
  pages permission system. This can be useful in a shared environment.
  By default a user can access all the smartsnippets in the system.

  If this setting is True the current user will only have access
  to smart snippets which are assigned to sites on which he as
  global page permissions. Otherwise the user will have acess to
  all smart snippets.

  For example, if the current user has global page permissions for
  Site1, Site2 and Site3, he will be allowed to edit smart snippets
  which belong to these three sites.

* ``SMARTSNIPPETS_CACHING_TIME`` is the number of seconds that
  rendered smart snippets will be cached. Defaults to 300. This can be used to
  greatly improve performance by removing the need for querying the database
  for variable values and skiping the template rendering logic. To
  disable the caching set this to 0. No caching is being done if logged
  in as a staff user.

.. WARNING::
  This plugin is a potential security hazard, since it allows admins to place
  custom JavaScript on pages. This may allow administrators with the right to
  add snippets to elevate their privileges to superusers. This plugin should
  only be used during the initial development phase for rapid prototyping and
  should be disabled on production sites.


.. _Twitter profile example:
    http://twitter.com/about/resources/widgets/widget_profile/

.. _django-cms:
    http://django-cms.org/

.. _snippet:
    http://readthedocs.org/docs/django-cms/en/latest/getting_started/plugin_reference.html#snippet

.. _django-cms demo:
    https://github.com/divio/django-cms-demo
