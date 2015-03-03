CHANGELOG
=========

Revision 82231f8 (03.03.2015, 12:28 UTC)
----------------------------------------

* LUN-2053

  * fixed resources ordering

No other commits.

Revision 8c07893 (29.01.2015, 15:42 UTC)
----------------------------------------

* LUN-2062

  * Style bentomatic andmin snippets vars

* LUN-2068

  * added pre/post validation events

* LUN-2072

  * variables shown need to belong to the current snippet set in the plugin

* LUN-2078

  * changed button labels; added confirm box on form submit

No other commits.

Revision 90290a3 (22.01.2015, 13:29 UTC)
----------------------------------------

* LUN-2069

  * variables rendering should access shared request context * passed plugin to context when editing its variables.

* Misc commits

  * qs has to be a list in order for + operand to work
  * static files and templates missing from package

Revision 81af772 (15.01.2015, 12:55 UTC)
----------------------------------------

* LUN-1954

  * confirm result looks better added in a variable.
  * no need for second dict update, used list concat instead
  * var names should be removed from context since there might be logic wich involves only context keys
  * overwrite variables editing now functional
  * added admin resources for variables forms
  * added view for variables edit
  * initial commit for new cms plugin which allowes other placeholder rendering

* Misc commits

  * no need for list casting on join for values list qs
  * removed unused templs; added current page for plugin form; CMSPLUGIN_INHERIT_NAME not required.
  * added js functionality to determine changed fields

Revision 821b9da (11.12.2014, 13:27 UTC)
----------------------------------------

* LUN-2008

  * improve performance for snippet vars save

No other commits.

Revision 703bd32 (03.12.2014, 14:31 UTC)
----------------------------------------

* LUN-1960

  * added events for snippet widgets lib
  * implemented js lib for snippet widgets registration inside plugin forms
  * implemented display for predefined widgets

* Misc commits

  * pep8 fix
  * add the ability to initialize/validate list of variables. * added required snippet js lib to model admin
  * added helper for snippet widgets js lib
  * added helper template tags
  * filter predefined vars to make sure they have data defined
  * don't render predefined vars unless they have widget or resources
  * hide predefined widgets when not available
  * fixed js custom exception + added variables getter utility
  * widget resources are now added to form media.
  * implemented functionality to expose global settings in template. Due to security issues django settings should not get exposed in templates (secret credentials might get stolen). What will get exposed in snippets settings will be up to the developer's decision.
  * fixed bugs with parsing resources; widgets media are now rendered
  * implemented functionality for parsing and using admin resources
  * removed unused template; * added resources field for snippet vars
  * default input should not be hidden. Users can define their own template for that
  * added new json hidden widget

Revision 8279fb9 (13.06.2014, 12:00 UTC)
----------------------------------------

* LUN-1591

  * preview will show snippet plugin with empty variables, even if the plugin was not saved yet

* LUN-1606

  * multiple exceptions must be specified as a parenthesized tuple.

* Misc commits

  * some var renaming.
  * User can now change snippet in change form, and the variables will get updated.

Revision ca3df43 (30.05.2014, 08:32 UTC)
----------------------------------------

* LUN-1580

  * Smart Snippet Plugins can now be build in one step.

* LUN-1581

  * changed text plugin icon for smart snippet

* Misc commits

  * some code style changes.
  * add icon and alt text
  * Set text_enabled for SmartSnippet

Revision 358e6d3 (17.04.2014, 13:23 UTC)
----------------------------------------

Changelog history starts here.
