# Design Considerations

I'm able to get a good grasp on big-picture stuff relatively easily. However,
I don't have a great memory for technical details, even stuff that I do
almost every day. I know people who are able memorize the fine details of
complex systems, and regurgitate them at will, sometimes years after the
fact. I'm not one of them.

To put it another way, I'm an idiot without my notes. This is my notebook.[^1]

[^1]: A few months after my first draft of this document, I learned that there
is a community of people who call this kind of software a [digital garden].

[digital garden]: https://github.com/MaggieAppleton/digital-gardeners/

I wrote this app to suit the way my particular brain wants to work. I have
tried many others and a few came close but didn't quite hit the spot. It took
a great deal to convince myself that it was worth my time to reinvent one of
the most commonly reinvented wheels. As a result, although I am definitely
intrested in improvements, what you see here is likely to stick. I'm not
inclined to add many bells and whistles because those things eventually
become known as "technical debt."

The following are a few of the _intentional_ design descisions and their
rationale.

## Function over Form

It's only natural that as technology progresses, innovation and novelty slow
down. As a result, many programs (even free and open source ones) attempt to
introduce novelty or stand out through visual design. This is the current
trend in software development, especially for personal productivity and
programming tools.

It's not hard to understand why. When you want users (or perhaps more often,
employers) to see your work, you need to grab their attention. The best way
to grab a person's attention is to show them something interesting.
Applications that _look_ interesting are desirable for that. It certainly
helps with "spreading the word" through our visual web and social media.

It's fine to develop a program as an art project, but the problem is that
when applications are developed as art projects, functionality almost always
suffers to some degree or another. When writing any kind of program, you
often have to choose between adding complexity to the UI, adding complexity
to the underlying code, or compromising on functionality. A person writing a
program to look pretty has already made those decisions up-front, usually in
favor of comprosmising on functionality because that involves shipping the
thing with the least amount of work.

Personally, I'd rather use an ugly tool that works well than a beautiful one
that slows me down or won't let me do my work the way I want to because it's
too busy checking itself in the mirror.

Things this app doesn't have and likely never will because they don't add
value to (or worse, subtract value from) my daily workflow:

* Emoji
* Things that fade in and out of existence
* Things that zoom around the screen for no reason at all
* Animated backgrounds
* Fancy-pants typography
* Scroll bar hijacking
* A front-end UI framework of any kind
* "Subscribe to my newsletter!"

## Web-Based

The app is web-based for the following reasons:

* All of my work is typically dependent on having an Internet connection anyway.

* Syncing notes between platforms is a hard problem, unless you delegate it to
something like Syncthing, which adds a layer of fragility and setup cost to
every platform you use to access your notes. Git is also a solution here, but
if you switch between several devices per day (like I do), then you're
constantly running (or forgetting to run) Git commands to keep your notes in
sync everywhere.

* I want to access my notes from my phone, without having to write an app.

* I want to access my notes from potentially _any_ computer without having to
install something special.

* I know how to write Python, HTML, CSS, and some Javascript.

* I self-host lots of other tools for myself and my family, adding another is
not a big deal for me.

* Web browsers tend to be very backwards compatible with old sites and apps,
(see: quirks mode) although the current leading browsers seem bent on
abandoning this. Still, the web is a much more stable API than any OS UI
toolkit in history.

## Dependencies: Few, Small, and Stable

Previous iterations of this app relied on bootstrap, jQuery, larger web
frameworks, etc. The problem with these is that they eventually age. Sure, you
can pin versions and just keep using them forever, and you might even get away
with it! But eventually a security vulnerability or incompatibility with a
modern version of the programming language comes to bite you. The problem is
compounded as your number of dependencies grow.

I plan on using this app for the rest of my life. But it's not a hobby. (I
have more than enough of those already!) There is a lot more I want to do
before my time on this planet runs out. I want to spend as little time as
possible maintaining this tool going forward, in order to allocate more time to
my family, friends, and hobbies (in that order).

To these ends, I am relying on dependencies that will save me greatly in up-
front costs (e.g. Flask) and shunning those that offer mainly convenience
(like an ORM, CSS toolkit, or flashy Javascript UI framework). I believe people
call this "boring technology" these days.

I chose dependencies that are relatively small, easy to understand, and if
not mature are at least apparently stable and therefore unlikely to change
dramatically in the future. I also hope that I have structured things in a
way that will make it relatively easy to swap out parts for better or more
available versions in the future.

## Markdown Syntax

I'll admit that I resisted using Markdown when it was just catching on because
it had all the hallmarks of a fad. I was wrong, and Markdown is not actually
half-bad, even if it is somewhat ill-defined. Many major sites and apps
promote (if not require) its use and I have since taken to writing Markdown
even in places where it will never be rendered into HTML, like text files and
emails.

Why not a WYSIWYG editor? A few reasons:

1. The lack of skill/desire to write one.
2. The lack of desire to pull one in as a dependency. (See above.)
3. The best WYSIWYG web editors tend to be buggy and have "edge cases" that I
seem to hit a lot.
4. I am a lot faster at getting my thoughts into writing with the needed style
cues inline, as text, than I am with keyboard shortcuts and clicking toolbar
icons.

## Least Cognitive Load

I use lots of software on a daily basis that tries to be everything to
everyone and as a result, cannot be customized for individual use cases. This
slows you down more than you realize until you've stood back to look at it.
Even small annoyances encountered frequently enough add up to significant
cognitive load that has no return on investment.

Prior to my iterations of this tool, all of my notes were kept in a
self-hosted instance of Dokuwiki. As open source wiki systems go, it's easily
at the top of the heap for being easy to set up and use. The main things that
took me away from it were the lack of native support for Markdown and the
editor UI.

_The editor UI, you say?_ Yes. Eventually, day by day, it managed to drive me
mad. You might think there's not much that can go wrong with a page that just
has a giant textarea and some buttons. But my notes pages get large in a hurry.
The page was always _just_ long enough to create a vertical scrollbar for the
main page, in addition to the inevitable textarea scrollbar. As improbable as
it sounds, dealing with two scrollbars started to become a distraction.

Yes, I could have re-themed Dokuwiki or something to solve this but I didn't
want to re-learn PHP and also learn how to hack on Dokuwiki, plus there were
other things I wanted out of it.

Another intentional design decision was omitting the ever-present changelog
line present in most wiki software. These are just my own notes, I don't have
to justify updating the content to myself. :)

## Data Permanance

SQLite

Reasons why plain text files didn't work out.

One of the reasons I liked Dokuwiki was that it was one of the few full-featured
wikis that did not need a database. You can just go to the data directory,
and there are your pages.

I was hoping to do something similar myself, but it turns out that you make
some trade-offs when you try to turn a file store into a document store:

* Want to keep every version of a page? Now you have to invent (or steal) a
file-based revision system. This alone almost nullifies the "simplicity"
argument for storing pages as files.

* Want to search all pages? Implementing a basic search feature on a tree of
files is not terribly difficult. But if you want search operators, you're left
with writing your own query parser, or bringing in a library to do it. When the
size if your notes collection grows, it also becomes important to index pages
so that you're not grepping over every byte in the tree for every search query.
Dokuwiki solved this by writing their own moderately complicated page index
system. You could pull in a full-text search application that does all of this
for you (e.g. ElasticSearch) but those tend to be quite heavy.

* If you later decide to add any metadata to pages beyond a title and timestamp,
you have to invent a way to store it.

After looking at all the options, I decided that storing pages in SQLite was
the best way to go for my purposes:

* Although the pages are "locked up" inside a database, SQLite is so mature
and ubuquitous that it seems like there is zero risk that the notes in the
database will ever be unreachable, no matter how far technology progresses in
the rest of my lifetime. It is fairly trivial to export the contents, should we
desire. (And we desire.)

* We can trivially implement page history by simply storing every edit to a page
as a new row in a table. The "current" version of a page is simply the one with
the newest timestamp. Listing, retrieving, and comparing old versions becomes
easy as well, as far as the data layer is concerned.

* SQLite has [rather amazing full-text-search](https://www.sqlite.org/fts5.html)
and indexing built right in! All you need are minor additions to your schema
and it Just Works.

* Extra page metadata is easy to add by just changing the schema and perhaps
some of your existing model code.

* Marginal benefit: One database file is easier to "handle" than a tree of
files, e.g. for backup or data migration purposes.

## Data Portability

Commands to export and import data.

## Search is King

Metadata curation is a hobby.

The "Related Pages" feature is the closest we get to curating metadata.

### Why can't I add tags to a page? Or put pages into a heirarchy or namespaces?

Previous iterations of this project supported these features. But I found
that no matter how hard I tried, I ended up using tags and page heirarchies
inconsistently across varous subjects. Some subjects lent themselves to a
nice obvious heirarchical system, others worked better with tags. Still
others didn't fit either well.

First I dropped support for tags because managing an accurate list of
relevant tags for each and every page, and reviewing them on every edit,
became a chore that I grew to loathe. Plus on the development side of things,
saving tags with each revision meant an extra layer of metadata. Since the FTS5
search engine in SQLite is excellent, tags became a labor-intensive redundant
feature.

Until I got rid of heirarchies too. I found that I only ever used them in one
section (my notes on Python) and found myself having to look up the linking
syntax involving namespaces every. Single. Time. Again, thanks to FTS5, I
found that I could do "soft" namespacing via page title prefixes (e.g.
"python_operators" instead of "python/operators") and just find everything I
need through the search which returns matches on both titles and body text.
These days, the pages that make up my section of Python notes look something
like this (after slugifying the page names):

* python
* python_operators
* python_functions
* python_classes
* python_virtual_environments
* (et al)

To put it another way, I want my database of notes to be a tool. They have
very low value on their own, but very high value in conjunction with my
day-to-day work. Any time spent "curating" them is time subtracted from
getting important things done.
