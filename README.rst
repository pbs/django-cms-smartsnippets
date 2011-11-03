Settings
========

There are three configuration variables available:

* ``SMARTSNIPPETS_SHARED_SITES`` a list of site names defaulting
  to an empty list. All the sites listed here will share theyr
  smartsnippets with all the other sites as read-only. This can be
  Usefull in a shared environment to enable code sharing.

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
