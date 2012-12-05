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

There are three configuration variables available:

* ``SMARTSNIPPETS_SHARED_SITES`` a list of site names defaulting
  to an empty list. All the sites listed here will share their
  smartsnippets with all the other sites as read-only. This can be
  Useful in a shared environment to enable code sharing.

* ``SMARTSNIPPETS_INCLUDE_ORPHAN`` a boolean flag that defaults to
  ``True``. If this option is enabled, selecting a site in the
  smartsnippet creation form is optional. If a smartsnippet doesn't
  belong to any site it will behave as global and will be available
  in all sites. If set to ``False`` the user will be forced to link
  the smartsnipptes that he creates to at least one site.

* ``SMARTSNIPPETS_RESTRICT_USER`` a boolean flag that defaults to
  ``False``. This flag, if set, will limit the smartsnippets that
  a user can access based on his relation to sites trough the global
  pages permission system. This can be useful in a shared environment.
  By default a user can access all the smartsnippets in the system.

* ``SMARTSNIPPETS_CACHING_TIME`` is the number of seconds that
  rendered smart snippets will be cached. Defaults to 3600. This can be used to
  greatly improve performance by removing the need for querying the database
  for variable values and skiping the template rendering logic. The cache is
  invalidated when any object involved in rendering a snippet changes. To
  disable the caching set this to 0.

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
