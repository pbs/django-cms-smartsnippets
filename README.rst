django-cms-smartsnippets
========================

``smartsnippets`` is a `django-cms`_ plugin similar to the builtin `snippet`_
plugin but instead of allowing only plain HTML you can use any valid
Django template syntax inside. When a smartsnippet is added in a page
the user can provide values for all detected used variables. This is much
more flexible than the standard ``snippet`` if you want to parametrize
and reuse your static snippets.

Example
=======

A simple smartsnippet using the `Twitter profile example`_::

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
          background: '#000000',
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
    }).render().setUser('{{twitter_username}}').start();
    </script>

Note the ``{{twitter_username}}`` variable used as a standard Django
variable. When adding the smartsnippet in a page, the form will
provide an input field where you can set a value of that variable.


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


.. _Twitter profile example:
    http://twitter.com/about/resources/widgets/widget_profile/

.. _django-cms:
    http://django-cms.org/

.. _snippet:
    http://readthedocs.org/docs/django-cms/en/latest/getting_started/plugin_reference.html#snippet
