# Design Considerations

I'm able to get a good grasp on big-picture stuff relatively easily. However,
I don't have a great memory for technical details, even stuff that I do
almost every day. I know people who are able memorize the fine details of
complex systems, and regurgitate them at will, sometimes years after the
fact. I'm not one of them.

To put it another way, I'm an idiot without my notes. This is my notebook.

I wrote this app to suit the way my particular brain wants to work. I have
tried many others and a few came close but didn't quite hit the spot. It took
a great deal to convince myself that it was worth my time to reinvent one of
the most commonly reinvented wheels. As a result, although I am definitely
intrested in improvements, what you see here is likely to stick. I'm not
inclined to add many bells and whistles because those things eventually
become known as "technical debt."

The following are a few of the _intentional_ design descisions and their
rationale.

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

I chose dependencies that are relatively small, easy to understand, and are
mature and therefore unlikely to change dramatically in the future. I also
hope that I have structured things in a way that will make it relatively easy
to swap out parts for better or more available versions in the future.

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

## Minimal Distractions

I use lots of software on a daily basis that tries to be everything to
everyone and as a result, much of it gets in your way a lot. Probably more
than you realize until you've stood back to look at it. Even small annoyances
encountered frequently enough add up to significant cognitive load that has
no return on investment.

Prior to my iterations of this tool, all of my notes were kept in a self-hosted
instance of Dokuwiki. As open source wiki systems go, it's easily at the top of
the heap for being easy to set up and easy to use. The main things that took me
away from it were the lack of native support for Markdown and the editor UI.

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

## Data Permenance

SQLite

Reasons why plain text files didn't work out.

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
