# mkdocs Test site

Static site generator with [mkdocs](https://www.mkdocs.org).  
PDF built with [mkdocs-with-pdf](https://github.com/orzih/mkdocs-with-pdf).  
Public URL: https://avdata99.github.io/test-mkdocs/  
PDF version: https://avdata99.github.io/test-mkdocs/pdf/doc.pdf  

## Build & Deploy

Using the [deploy-mkdocs](https://github.com/marketplace/actions/deploy-mkdocs)
GitHub action a public html site will be built.  

## Features

The `docs` folder include markdown files that will be built as a html site and a PDF document. 
It's also possible to include static files.  
The `mkdocs.yml` file allows you to define all the site and PDF settings.  
The `pdf-template` folder include the cover and back-cover html files that will be used only in the PDF version. It's also posible to define custom CSS style for the PDF version with the `styles.scss` file.  
