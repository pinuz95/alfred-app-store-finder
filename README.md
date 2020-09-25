App Store Finder for [Alfred](http://www.alfredapp.com)
==============================

Find any app in the App Store and paste its app ID.

## Usage

Use the command `app` to find an app. You can select (click or press enter) an app to copy-paste its app ID.
Use the command `app bundle` to copy-paste the bundle ID of an app. You can also use `app id`, that is equivalent to `app`.

### Commands
* `app [bundle/id] <app name> [<storefront>]`
* `app [bundle/id] <app ID>`

### Examples
* `command` -> `pasted string`

* `app pic jointer` -> `509987785`
* `app id pic jointer` -> `509987785`
* `app bundle pic jointer` -> `com.lileping.photoframepro`
* `app 30 day fitness it` -> `1099771240`
* `app bundle stepz gb` -> `com.visualhype.pedometer`
* `app 409838725` -> `409838725`
* `app bundle 1148951074` -> `com.flyingnayeem.yoga`

You can specify a storefront to find the app name in that specific storefront. Please notice that the apps are _not_ ordered according to the App Store search results.

**[Latest release](https://github.com/pinuz95/alfred-app-store-finder/releases)**

![Workflow Screenshot](screenshot.png)
