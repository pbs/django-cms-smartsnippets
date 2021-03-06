CHANGELOG
=========

Revision 5da99c1 (04.10.2019, 15:40 UTC)
----------------------------------------

No new issues.

* Misc commits

  * Pin attrs to 19.1.0

Revision 15edf0e (06.11.2018, 09:54 UTC)
----------------------------------------

No new issues.

* Misc commits

  * Pin pytest 3.4.0 and pytest-django 3.1.2

Revision e961257 (13.02.2018, 12:56 UTC)
----------------------------------------

No new issues.

* Misc commits

  * Fixed migration
  * Fixed migration

Revision 195f80b (05.02.2018, 15:47 UTC)
----------------------------------------

No new issues.

* Misc commits

  * Added migration to update custom components name and description

Revision 62c8387 (14.02.2017, 12:14 UTC)
----------------------------------------

* LUN-3440

  * add spacing for submit buttons admin form

No other commits.

Revision 0ed55d3 (26.08.2016, 07:27 UTC)
----------------------------------------

* LUN-3023

  * Handle input fields that do not have classes.
  * Allow closing the window without validating fields.
  * Improve handling for incorrect rendering.
  * Review improvements.
  * Fix saving issues and add url for edit.
  * Review refactoring and fixes.
  * Add tag that renders a smartsnippet based on a JSON configuration.
  * Add alternative admin rendering based on JSON configuration serializing/deserializing.

* LUN-3167

  * Apply Json handling to the hero fields also.

No other commits.

Revision 4996793 (06.05.2016, 15:19 UTC)
----------------------------------------

* LUN-2549

  * Update plugininherit_change_form.html
  * Update tooltips.

* LUN-2594

  * Update change_form.html

* LUN-2791

  * Fix typo.
  * Add tests for handling snippet rendering errors.
  * Show warnings when snippets cannot be rendered.

No other commits.

Revision 2cbe661 (08.04.2016, 07:13 UTC)
----------------------------------------

* LUN-2549

  * Add migration for field new verbose name.

* Misc commits

  * Update setup.py version to 1.4.0.
  * Lun-2549: Rename smartsnippet to custom component.

Revision b091703 (03.02.2016, 07:32 UTC)
----------------------------------------

* LUN-2549

  * Revert "LUN-2549: changed name for smartsnippets to components"

No other commits.

Revision fb950ce (14.01.2016, 13:22 UTC)
----------------------------------------

* LUN-2549

  * changed name for smartsnippets to components

* Misc commits

  * Limit django-sekizai version to last one working.
  * Add merge migration.

Revision 0f57a0d (04.11.2015, 15:03 UTC)
----------------------------------------

* LUN-2477

  * remove custom style of popover text, left default from ace
  * if no documentation link, description was not interpreting html

* LUN-2550

  * Fix typo.
  * Narrow the allowed URLs.
  * Clean imports.
  * Add URLField widget.

* LUN-2771

  * Support obsolete ordering by name if _order remains 0.

* Misc commits

  * Update pattern and messages for URL field validation.

Revision 2ac0965 (28.10.2015, 12:01 UTC)
----------------------------------------

* LUN-2238

  *  LUN-2238: Add position field to smartsnippet variables.

* Misc commits

  * Added merge migration for parallel changes.
  * Add migration for order_with_respect_to.
  * Shorten code lines.
  * Support drag and drop for smartsnippet variable reordering.
  * Remove unused import.

Revision 6a793c1 (01.10.2015, 12:21 UTC)
----------------------------------------

* LUN-2679

  * hide related buttons for snippet field on plugin form

No other commits.

Revision c7df47c (23.09.2015, 15:30 UTC)
----------------------------------------

No new issues.

* Misc commits

  * Django 1.8 upgrade: updated admin templates
  * Django 1.8 upgrade: removed some django1.9 deprecation warnings
  * Django 1.8 support: fixed tests failing since RequestContext must be bounded to a template in order for the template processors to be executed

Revision 52c96af (11.09.2015, 13:58 UTC)
----------------------------------------

No new issues.

* Misc commits

  * 2620: misspelled help_text fixed

Revision bb811eb (04.09.2015, 09:01 UTC)
----------------------------------------

* LUN-2291

  * fixes for Ace theme on bentomatic
  * added forgotten active class for selected tab
  * allow ace theme for admin plugin form

* LUN-2579

  * refactor change_form, fixed breadcrumbs

* LUN-2596

  * fieldset columns width updated

No other commits.

Revision 2f33933 (28.08.2015, 07:21 UTC)
----------------------------------------

* LUN-2310

  * refactor Media resources
  * fielset refactoring
  * removed get_setting tag due to security issues
  * added newline at the end of tags.py file
  * fieldset updated for non-ace theme
  * removed custom breadcrumbs
  * toggle resources based on active Ace theme or not
  * error messages fix
  * refactoring of html to match Ace theme
  * preview link text and background changed
  * breadcrumbs updated

* LUN-2325

  * Make snippet documentation link and description visible event if snippet doesn't have variables

* LUN-2564

  * added -safe- filter for smartsnippet_description
  * striptags from smartsnippet_description

* Misc commits

  * master Added missing migration for changes to help_text.
  * master Removed git ignore for py files.

Revision 2d692b6 (03.08.2015, 09:13 UTC)
----------------------------------------

* LUN-2235

  * Simplified the logic for detecting duplicate variable names.
  * Better error message for duplicate variable names.
  * Reordered imports.
  * Added validation message for multiple duplicate variable names.
  * Documented workaround for testing.
  * Reordered imports.
  * Added tests for variable name handling.
  * Validate that variable names are unique in all the inlines.
  * Cleaned the variable names before saving.

* Misc commits

  * Added more tests with valid variable names.
  * Removed print.

Revision 9b2f779 (24.07.2015, 14:44 UTC)
----------------------------------------

No new issues.

* Misc commits

  * No need for line breaks

Revision bf714da (17.07.2015, 13:28 UTC)
----------------------------------------

No new issues.

* Misc commits

  * tox: Don't allow django 1.8 prereleases
  * changed static files urls in order for them to work with other static files storages
  * s3sourceuploader no longer required
  * Django 1.7 upgrade: fixed migrations & tests
  * Django 1.7 upgrade: fixed deprecation warnings; fixed module_name
  * Django 1.6 upgrade; fixed url templatetag
  * Django 1.6 upgrade: fixed change_view & adminmedia tag

Revision 37ed35d (15.07.2015, 07:29 UTC)
----------------------------------------

* LUN-2401

  * create new filter to get item from json array by index

No other commits.

Revision fa079bb (03.07.2015, 13:12 UTC)
----------------------------------------

* LUN-2371

  * Open snippet documentation link in new tab/window

No other commits.

Revision f9511af (19.06.2015, 05:28 UTC)
----------------------------------------

* LUN-2227

  * set default style for textareas
  * default dark color set to all inputs/dropdowns/textareas
  * added image for draggable items
  * added pbs overrides for bootstrap and ace themes
  * add missing js files
  * small js and css updates
  * new SwitcherField created for all smartsnippets
  * Added Ace theme to all smartsnippets
  * moved code around to allow bootstrap ACE theme to work

* LUN-2228

  * Display the correct documentation and set the correct smartsnippet documentation url when adding a new smartsnippet.

* Misc commits

  * added MANIFEST.in and .gitignore
  * typo misspelling of bootstrap
  * default style for disabled buttons set

Revision 9a027c8 (23.04.2015, 07:45 UTC)
----------------------------------------

No new issues.

* Misc commits

  * exclude_empty should always exlude empty items before key/attr exclusion; from_context should not change value even if empty
  * added docs + renamed funcs to be more explicit
  * added custom helper filters

Revision f5607ba (08.04.2015, 11:19 UTC)
----------------------------------------

* LUN-2115

  * New assigment_tag created so we can take variables from context
  * timestamp template tag created

* LUN-2130

  * Don't validate snippet fields when cancel is pressed

No other commits.

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
