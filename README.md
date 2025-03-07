# README

Demo at
* [https://oberron.github.io/spark-fi/](https://oberron.github.io/spark-fi/)

## About

No spark is too small to fire a dream


## SETUP/CONFIG

* Wrapper around Pelican for deployments and Notion synchronisation
* Pelican based blogging platform for blog entries in /content
* Requires py>=3.12

#### Features

* Sitemap and XML Feed
* Pagination in homepage
* Posts under category
* Category page with descriptoin (relies on a page with the same name as category, see category.html: `page.title == category.name`)
* Realtime Search Posts _(title & description)_ by query.
* Related Posts
* Next & Previous Post
* Projects page & Detail Project page

### How to Use?

**a. Add new Category**

All categories saved inside path of `category/`, you can see the existed categories.

**b. Add new Posts**

* All posts bassed on markdown syntax _(please googling)_. allowed extensions is `*.markdown` or `*.md`.
* This files can found at the path of `_posts/`.
* and the name of files are following `<date:%Y-%m-%d>-<slug>.<extension>`, for example:

```
2013-09-23-welcome-to-jekyll.md

# or

2013-09-23-welcome-to-jekyll.markdown
```

Inside the file of it,

```
---
layout: post                          # (require) default post layout
title: "Your Title"                   # (require) a string title
date: 2016-04-20 19:51:02 +0700       # (require) a post date
categories: [python, django]          # (custom) some categories, but makesure these categories already exists inside path of `category/`
tags: [foo, bar]                      # (custom) tags only for meta `property="article:tag"`
image: Broadcast_Mail.png             # (custom) image only for meta `property="og:image"`, save your image inside path of `static/img/_posts`
---

# your content post with markdown syntax goes here...
```

### BUILD SITE

1. locally

to update podcast only or validate the podcast.xml generated:

> python wrapper.py -p -l

2. github

> python wrapper.py -g -t -p

### KNOWN Bugs

* baseurl calculation in the different .js does not work in daughter page, compensation for baseurl if not CNAME only works on homepage