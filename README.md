[![Publish docs via GitHub Pages](https://github.com/okfn/okfn-collaborative-docs/actions/workflows/page.yml/badge.svg)](https://github.com/okfn/okfn-collaborative-docs/actions/workflows/page.yml)

# mkdocs Test site

This template is still in progress.  

Static site generator with [mkdocs](https://www.mkdocs.org).  
PDF built with [mkdocs-with-pdf](https://github.com/orzih/mkdocs-with-pdf).  
Public URL: https://okfn.github.io/okfn-collaborative-docs/  
PDF version: https://okfn.github.io/okfn-collaborative-docs/pdf/doc.pdf  

## Build & Deploy

Using the [deploy-mkdocs](https://github.com/marketplace/actions/deploy-mkdocs)
GitHub action a public html site will be built.  

## Features

The `docs` folder include markdown files that will be built as a html site and a PDF document. 
It's also possible to include static files.  
The `mkdocs.yml` file allows you to define all the site and PDF settings.  
The `pdf-template` folder include the cover and back-cover html files that will be used only in the PDF version. It's also posible to define custom CSS style for the PDF version with the `styles.scss` file.  
Translations are [availabe](https://www.mkdocs.org/dev-guide/translations/) for mkdocs.  

# How to create new documentation

Steps to get you page and PDF done:

 - Create a new repo from the [base template](https://github.com/okfn/okfn-collaborative-docs)
 - Modify ``index.md`` at ``docs`` and ``docs-es``
 - Create new md files at ``docs`` and ``docs-es`` folders
    - Include them at ``nav`` section at ``mkdocs-en.yml`` and ``mkdocs-es.yml``
 - Put static content at the ``assets`` folder (images, css, js, etc).  
 - Replace mkdocs files: okfn-collaborative-docs -> testing-mkdocs-multilang-template **TODO**
 - Enable the ``gh-pages`` branch to be published as GitHub Pages
 - Push! (all languages will be built automatically)

## TODOs

Requirements or possible new features:
 
 - Include a PDF link in the header
 - FIX: The edit icon for each page point always to english version
 - Add a step to update github URL and repo name in mkdoc files automatically
 - Allow add or remove languages with a single command
 - Check style for `es` language
 - Allow defining all settings in a custom file and build automatically all required mkdocs-LANG files
