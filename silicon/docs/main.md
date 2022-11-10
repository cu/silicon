Welcome to the documentation for Silicon Notes, a low-friction personal knowledge base.

This page is a brief introduction to the program. For a detailed reference on the syntax supported, see the [Markdown Syntax](/docs/syntax) documentation.

# Layout

There are two main parts to the interface:

1. A nav pane on the left containing navigation controls and metadata about the current page being viewed or edited.
2. A larger "content" pane on the left that contains the page text rendered in HTML, or an editor when the page is being edited, or other content depending on which part of the program you are in.

When the browser window is narrow, the UI automatically changes to a "mobile" view which is laid out the same except that nav pane is hidden by default. To see it, click the Nav button at the top. To get back to the content pane, click the Nav button again.

The nav pane contains a number of features which are described in more detail below. These change depending on where you are in the interface but most of the time you will see the following:

* The name of the page currently displayed.
* Some navigation links for getting around the program.
* A prominent Edit button for editing the current page.
* A timestamp showing when the current page was last edited.
* A Related section showing which other pages are related to the current page.
* A Contents section showsing a table of contents for the headings in the current page.

# Pages

Pages are the foundation of this knowledge base. It is suggested that you have one page per note, but you can actually have as few or as many pages as you like.

The top line of the nav pane shows the page name. All page names are automatically lowercased and all whitespace and symbols are replaced with underscores. This makes it easier to link to pages without having to remember how the names were capitalized or whether they included some kind of punctuation. This also makes the URLs for individual pages better to work with.

# Editing and History

To add a page, click the Edit button in the nav pane. This will take you to an editor that lets you edit the page as plaintext in Markdown. If you don't know Markdown, it is very easy to learn. See the [Markdown Syntax](/docs/syntax) for full details and examples on all of the supported features.

Every time you edit a page, make some changes, and save the result, a new revision of the page is created. You can see the revision history of a page by clicking on the History link in the left pane. When viewing a page, a timestamp showing the most recent revision of the page is shown in the left pane.

The "front" or "main" page of the wiki is called `home`. This page is the same as any other page you might choose to create/edit, with two exceptions:

1. If the path is missing from the URL, the application will automatically redirect to it.
2. There is a link to it in the nav pane, so you can get back to it wherever you wind up in the program.

# Internal Links

You will likely want to have multiple pages and to create links to some of those pages from other pages. The way to do that is with an internal link. A sentence with an internal link to another page looks like this:

```
Gently fold [[Fresh Strawberries]] into the custard.
```

You simply surround the name of the page you want to link to with a matching pair of double square brackets. The program will understand that this is a page name and automatically create a link to it, even if the page does not already exist.

When the sentence above is saved and then viewed, it will look like this:

> Gently fold [Fresh Strawberries](/view/fresh_strawberries) into the custard.

If you hover over the link (and if your browser shows URLs when you hover over them), you will see the page name in the URL and you will notice that the page name has been made lowercase and the space replaced with an underscore.

You can find out more about internal links in the [syntax](/docs/syntax) documentation page.

# Related Pages

The nav pane has a section called Related. You can use this to create two-way relationships between pages. For example, if you store your cooking notes here, you might have a page called `fruit` with general techniques and also two other pages for nitty-gritty details of `pears` and `cantaloupe`.

You certainly _could_ edit the `fruit` page and manually add internal links to `pears`, `cantaloupe`, and any other fruit you work with somewhere in the page. And then for completeness, you might want to link _back_ to the `fruit`
page from the more topic-specific pages, which requires editing those pages as well.

The easier way is to add them as related pages. From the `fruit` page, just click the "add" text next to "Related" in the nav pane. Enter the name of the page to create a relationship to (say, `pears`) and hit OK. Now there is a
two-way relationship between the `fruit` page and the `pears` page. If you go to either one, the other will show up in the Related section.

Relationships are easy to remove simply by hovering over them and clicking the "remove" text that appears to the right of the page name.

The nice thing about the Related section is that you can add or remove relationships while viewing or editing a page without reloading the page.

# Table of Contents

The Contents section in the nav pane displays a list of all of the headings in the current page. If there are no headings, this section will be empty.

If you click on a heading, you will be taken to that heading in the page, and your browser window will scroll to it if necessary.

When editing a page, the table of contents is not updated automatically as you enter text. However, you can update the table of contents by clicking on "update" at the top of the CONTENTS section. Clicking on the links in the CONTENTS section does not navigate you to that section while editing a page.

# Search

The search field at the bottom of the nav pane allows you to perform a search of the entire notes database. Simply type in your search query and hit Enter.

The search results screen has two sections: one that shows results for page titles that matched your query and other that shows results for text in the page body that mathched your query. The parts of your query that matched the page title or body are highlighted in the results.

A brief list of search tips appears in the nav pane, but here is a slightly more detailed explanation of the options:

* Search terms are case-insensitive which means the program pays no attention to whether any letters you enter are uppercase or lowercase, and matches the words in the page titles or body whether they are uppercase or lowercase as well.

* When you enter multiple words, **both** must appear in the title or body in order to appear in the results. For example, if you enter `blueberries strawberries` as a search query, you will only get results for titles and pages that contain _both_ `blueberries` and `strawberries` somewhere in them.

* When you enter multiple words separated by `OR` (which must be uppercase), that tells the search engine to match either one. If you enter a query of `huckleberries OR raspberries`, you will get results for titles and pages that have **either one** of `huckleberries` or `raspberries` in them.

* You can prefix a word with the special operator `NOT` (which must be uppercase), that tells the search engine to **exclude** pages containing that word. Say you were to enter in a query of `blackberries NOT kiwi`, you would only get pages that had the word `blackberries` in it _as long as_ they did not also have the word `kiwi` in them anywhere.

* If you want to search for a particular **phrase** (multiple words together) only, surround the phrase with double quotes. A search query of `"apples peaches pumpkin pie"` will only return titles and pages with those four words right next to each other, in that order.

* To search for any words **starting with a specific set of letters**, enter the prefix followed by an asterisk (`*`). For example, a query of `past*` will find titles and body text containing the words `pasta`, `pastry`, and so on.

* If you know that the page title or body you want **starts with a certain word**, you can prefix the caret (`^`) to that word in your query. If your search query is `^cookies`, the results might contain a page title or body that started with `cookies and cream` but not `chocolate chip cookies`.

For more power in finding your notes, any of the above can be combined into a single query. For example:

* `cookies OR brownies OR tarts` will match any page containing any of those words.

* `donuts NOT "vanilla custard"` will only match pages containg the word `donuts` but will not match any pages containing the whole phrase `vanilla custard`, even if they also have `donut` in them.

* `pie cru*` will match pages that contain _both_ the word `pie` and any word that starts with "cru", such as `crust`, `crunch`, or `crumble`.

