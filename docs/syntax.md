This page describes the supported Markdown syntax and functionality in full
detail. If you would like a shorter guide to reference for some of the more
basic syntax, see https://commonmark.org/help/.

# Inline Markup

Inline markup affects spans of regular text.

```
Italic text is surrounded by *asterisks* or _underscores_.

Bold text is surround by **double astersisks** or __double underscores__.

Strikethough uses ~~two tildes~~.

This is an example of combined _italic, **bold, and ~~strikethrough~~**_.

Monospace text is surrounded by `backticks`.
```

Italic text is surrounded by *asterisks* or _underscores_.

Bold text is surrounded by **double astersisks** or __double underscores__.

Strikethough text is surrouned by ~~two tildes~~.

Monospace text is surrounded by `backticks`.

This is an example of combined _italic, **bold, and ~~strikethrough~~**_.


# Horizontal Rules

HRs are three or more dashes, asterisks, or underscores on their own line.

```
---
***
___
```

---
***
___


# Paragraphs

Paragraphs are separated by two consecutive line breaks. Text separated by a single line break will render as one combined paragraph with a single space in place of the newline. If you want to insert a line break without creating a new paragraph, use two trailing spaces before the line break:

```
Paragraph One.

Paragraph Two.

This is a paragraph with three lines
and a single line break separating them.
They are rendered into the same paragraph.

To force a line break without a paragraph, use  
two trailing spaces at the end of the previous line.
```

Paragraph One.

Paragraph Two.

This is a paragraph with three lines
and a single line break separating them.
They are rendered into the same paragraph.

To force a line break without a paragraph, use  
two trailing spaces at the end of the previous line.  


# Headings

_(Rendering of headings in this section is ommitted for clarity.)_

Headings are prefixed with one hash symbol for each level.

Alternatively, headings can be underlined by equals signs and dashes.

```
# Heading 1
## Heading 2
### Heading 3
#### Heading 4
##### Heading 5
###### Heading 6

Heading A
=========

Heading B
---------
```

# Lists

```
* Unordered lists prefixed with an asterisk.
- Or a dash.
+ Or a plus.
* And the next item in the list continues on the line immediately below it.
* Separate lists must be separated by a blank line or a different list prefix symbol.

1. ordered lists
1. are prefixed with an integer and dot

* both kinds of lists can have nested items via indentation
  * a tab or two or more spaces can be used,
  * as long as they are used consistently within the same list

* You can have paragraphs within list items...

  ...if you indent the paragraph to the same level as the list text.  
  
  To insert a line break without leaving the list, append two trailing
  spaces to the previous paragraph.
```

* Unordered lists prefixed with an asterisk.
- Or a dash.
+ Or a plus.
* And the next item in the list continues on the line immediately below it.
* Separate lists must be separated by a blank line or a different list prefix symbol.

1. ordered lists
1. are prefixed with an integer and dot

* both kinds of lists can have nested items via indentation
  * any number of spaces and tabs can be used,
  * as long as they are used consistently within the same list

* You can have paragraphs within list items...

  ...if you indent the paragraph to the same level as the list text.  
  
  To insert a line break without leaving the list, append two trailing spaces to the previous paragraph.


# Definition Lists

Definition lists are useful when you have a word or short phrase along with some descriptive text below it.

```
First term
: First definition
: Second definition

Second term
: Third definition
```

First term
: First definition
: Second definition

Second term
: Third definition


# Links

## External Links

### Bare URLs

Bare URLs are turned into links, as are URLs enclosed in angle brackets.

```
Bare URL: https://www.example.com/

Bare URL with angle brackets: <https://www.example.com>
```

Bare URL: https://www.example.com/

Bare URL with angle brackets: <https://www.example.com>

### Inline-Style Links

Inline links have the link text in square brackets followed by the URL in parentheses. They can also have a title in quotes after the URL, which shows a pop-up containing the title in most browsers.

```
[link text](https://www.example.com/)

[link text](https://www.example.com "Link Title")
```

[link text](https://www.example.com/)

[link text](https://www.example.com "Link Title")


### Reference-Style Links

Reference style links use an identifier to locate the URLs themselves elsewhere in the document, perhaps after a paragraph or at the end of the page. The identifier is an arbitrary alphanumeric string with optional whitespaces, but integer numbers and short phrases are common. You can also omit the identifier and use the link text as the identifier. The URLs themselves are not rendered.

```
A reference link: [link text][identifier text]

A reference link with [just link text]

[identifier text]: https://www.example.com
[just link text]: https://www.example.com
```

A reference link: [link text][identifier text]

A reference link with [just link text]

[identifier text]: https://www.example.com
[just link text]: https://www.example.com

### Image Links

Links to inline images work exactly like the external links above, except they are prefixed with a bang (`!`) and the link text becomes the image's alt text.

```
![alt text](https://www.example.com/image.png)
```

## Wiki-style Links

Links to other pages are enclosed in double square brackets.

```
[[example]]
```

[[example]]

Links to pages are "slugified", meaning that the link text is "normalized" into a page name so that link to a particular page can have variations in letter case, special symbols, and so on in the link text. The most important rules are:

* All letters are converteed into lowercase
* Spaces and most symbols are converted into underscores.
* Contiguous strings of non-alphanumeric characters are converted into a single underscore

```
[[Link Text With Capital Letters]] becomes the page name
`link_text_with_capital_letters`

[[Symbols & Spaces Become Underscores]] becomes
`symbols_spaces_become_underscores`

[[C++ & C# & Suchlike]] becomes `c_and_c_suchlike`
```

[[Link Text With Capital Letters]] becomes the page name `link_text_with_capital_letters`

[[Symbols & Spaces Become Underscores]] becomes `symbols_spaces_become_underscores`

[[C++ & C# & Suchlike]] becomes `c_and_c_suchlike`

### Alternate Text

Every kind of wiki link above can have alternate link text by adding a pipe (`|`) and a string. The link is then rendered with that string instead of the one specified as the link.

```
[[Python|Batteries Included!]]
```

[[Python|Batteries Included!]]


# Footnotes

Footnotes allow you to add notes and references to a page without cluttering up the main content. They are links to specific items at the bottom of the page. To create a footnote, add a caret and an identifier inside square brackets (`[^1]`). The identifier can be a number or alphanumeric string with optional whitespaces.

For the content of the footnote, prefix the footnote with a caret and identifier inside square brackets followed by a colon (`[^1]:`), and then add the footnote content following that. Multiple paragraphs can be added to the footnote content by indenting them with one or more spaces.

To see the example footnotes, scroll to the bottom of this document.

```
This is a footnote,[^1] and here is another.[^another note]

[^1]: This is the first footnote.

[^another note]: This is one with multiple paragraphs and code.

 Indent paragraphs to include them in the footnote.

 Footnote paragraphs can have inline styles such as _italic_ and `monospace`.
```

This is a footnote,[^1] and here is another.[^another note]

[^1]: This is the first footnote.

[^another note]: This is one with multiple paragraphs and code.

 Indent paragraphs to include them in the footnote.

 Footnote paragraphs can have inline styles such as _italic_ and `monospace`.


# Abbreviations

Abbreviations can be defined with an asterisk, followed by the abbreviation in square brackets, followed by a colon, and the expanded defintion, name, or phrase. In most browsers, when you hover over the abbreviation, the definition pops up under the mouse cursor as a tooltip.

```
The HTML specification is maintained by the W3C.

*[HTML]: Hyper Text Markup Language
*[W3C]: World Wide Web Consortium
```

The HTML specification is maintained by the W3C.

*[HTML]: Hyper Text Markup Language
*[W3C]: World Wide Web Consortium


# Preformatted Text

To specify a block of pre-formatted text to be rendered in a monospace
font, put it between two triple-backticks, each on their own line.

You can also prefix each line by four spaces to achieve the same effect.

<pre>
```
1 2 3 4 5
a b c e f
g h i j k

  l m n o p
  q r s t u
```
</pre>

```
1 2 3 4 5
a b c e f
g h i j k
```

    l m n o p
    q r s t u

## Code Blocks

Blocks of code and other markup will be syntax-highlighted if you tag the
code block with a well-known language name by placing it after the first
set of triple backticks.

An example with bash:

<pre>
```bash
#!/usr/bin/env bash
echo "Hello!"
```
</pre>

```bash
#!/usr/bin/env bash
echo "Hello!"
```

An example with Python:

<pre>
```python
import sys
print('spam', file=sys.stderr)
```
</pre>

```python
import sys
print('spam', file=sys.stderr)
```

[Pygments](https://pygments.org/) is used for the syntax highlighting, check [its documentation](https://pygments.org/languages/) for details on supported languages. The best source for which tags map to which languages seems to be [this file](https://github.com/pygments/pygments/blob/master/pygments/lexers/_mapping.py).


# Block quotes

Blocks of quoted text are prefixed with a right angle bracket (`>`) followed by a space. Multiple levels of quoting are supported by adding additional right angle brackets.

```
> This is a quoted block of text.

>> This is the second level of quoted text.

>>> This is a third level of quoted text.
```

> This is a quoted block of text.

>> This is the second level of quoted text.

>>> This is a third level of quoted text.


# Tables

Every table must consist of:

* A header, with a pipe symbol (`|`) surrounded by at least one space between each column name
* A header divider consisting of three or more dashes (`---`) in each cell
* At least one row, with each cell separated by a pipe symbol

Cell contents are left-aligned by default. Column contents can be centered by replacing the header divider cell spaces with colons (`:`) on each end, or right-aligned by replacing the right space with a colon. Text can also be right-aligned by placing it towards the right of the cell.

The cells do not have to align vertically in the markup, but they are easier to read that way.

The outer pipes are optional.

Basic table:

```
| First Header  | Second Header |
| ------------- | ------------- |
| Content Cell  | Content Cell  |
```

| First Header  | Second Header |
| ------------- | ------------- |
| Content Cell  | Content Cell  |

Table with centered and right-aligned text:

```
| Name      | Vocation | Amount |
| ----      |:--------:| ------:|
| Chris     | Coder    | $99    |
| Drew      | UI       | $42    |
| Kelly     | QA       | $13    |
| Mackenzie | PM       | $88    |
```

| Name      | Vocation | Amount |
| ----      |:--------:| ------:|
| Chris     | Coder    | $99    |
| Drew      | UI       | $42    |
| Kelly     | QA       | $13    |
| Mackenzie | PM       | $88    |

Minimal table:

```
1|2
---|---
foobar|baz
```
1|2
---|---
foobar|baz


# HTML, CSS, and Javascript

Raw HTML, CSS, and Javascript can be used where convenient or necessary.

```
<b>bold</b> and <i>italic</i>

A link to <a href="https://example.com">example.com</a>.

<h3>Heading 3</h3>

Tiny raised text: <sup>superscript</sup>

Tiny lowered text: <sub>subscript</sub>

<hr>

<p>Click the button to swap the text of the DIV element:
<button onclick="myFunction()">Click Me</button></p>

<div id="myDIV">Hello</div>

<script>
function myFunction() {
  var x = document.getElementById("myDIV");
  if (x.innerHTML === "Hello") {
    x.innerHTML = "World!";
  } else {
    x.innerHTML = "Hello";
  }
}
</script>
```

<b>bold</b> and <i>italic</i>

A link to <a href="https://example.com">example.com</a>.

<h3>Heading 3</h3>

Tiny raised text: <sup>superscript</sup>

Tiny lowered text: <sub>subscript</sub>

<hr>

<p>Click the button to swap the text of the DIV element:
<button onclick="myFunction()">Click Me</button></p>

<div id="myDIV">Hello</div>

<script>
function myFunction() {
  var x = document.getElementById("myDIV");
  if (x.innerHTML === "Hello") {
    x.innerHTML = "World!";
  } else {
    x.innerHTML = "Hello";
  }
}
</script>
