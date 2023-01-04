[![Publish docs via GitHub Pages](https://github.com/okfn/okfn-collaborative-docs/actions/workflows/page.yml/badge.svg)](https://github.com/okfn/okfn-collaborative-docs/actions/workflows/page.yml)
[![Tests](https://github.com/okfn/okfn-collaborative-docs/actions/workflows/tests.yml/badge.svg)](https://github.com/okfn/okfn-collaborative-docs/actions/workflows/tests.yml)

# OKFN Collaborative Documentation tool

This is a GitHub template to create multilanguage collaborative documentation with a
public html site and a PDF version. It's based on [mkdocs](https://www.mkdocs.org).   

## Creating my first documentation

At this [repo url](https://github.com/okfn/okfn-collaborative-docs/)
click on the _Use this template_ + _Create new repository_ button
or go directly to the [generate from template url](https://github.com/okfn/okfn-collaborative-docs/generate)

![Use template](docs/imgs/use-template.png)

Do not forget to define your new repository as **Public**.  

### Prepare your local environment.

Clone your new pository and install the project requirements.
This is an example for Linux/Ubuntu:

```bash
# Clone your new repository 
git clone git@github.com:YOUR-ORG/YOUR-REPO-NAME.git
# Create a Python3 virtual environment
python3 -m venv /path/to/new/virtual/environment
# Activate the virtual environment
source /path/to/new/virtual/environment/bin/activate
# Install the project requirements
cd YOUR-REPO-NAME
pip install -r requirements.txt
``` 

### Define your custom settings

Your main configuration file is `/conf/custom.yml`.  

#### Languages

First of all, you need to define your site name and the languages you want to use.  
Define languages at `custom_extra`->`alternate` and the site name at `site_name`.  

```yaml
custom_extra:
  # define all available languages
  alternate:
    - name: English
      lang: en
    - name: Español
      lang: es
```

```yaml
site_name:
    en: My site name
    es: Mi sitio
```

You can add as many languages as you want. 
All languages will be required for other multilanguage configurations.  

#### URL settings

Now, define your GitHub (required) settings.

You can automatically update your repository settings with:

```bash
python3 okf_collab_docs/run.py init
```
(this command will also initialize your README.md file for you)

Or manually change these settings:

```yaml
repo_user: your-github-user-or-org-name
repo_name: you-new-repo-name
```
_Note:_ `repo_user` and `repo_name` came from your new GitHub repository url: https://github.com/REPO_USER/REPO_NAME

If you plan to use the default GitHub domain, you are done with this settings.  
The site will be available at https://USER.github.io/YOU-REPO-NAME.  
Conversely, if you plan to use a custom domain, you'll need something like this:

```yaml
# Only for custom domains you can use:
custom_site_url: https://your-site.org
# public_url_base_path: /some-base-path-folder (only if required)
```
_Note:_ You'll need a CNAME record pointing to `USER.github.io`

#### Other settings

The `site_description`, `copyright` and `site_author` are self-explanatory.  

If you need to define custom context values to use in your templates, you can do it with the `custom_extra` setting.  

Some examples:

```yaml
custom_extra:

  # other custom extras (like alternate for )...
  # define custom context values

  my_value: Some text (will be available for all .md and .html files as {{ my_value }})
  my_dict:
    some_key: "my custom value in english" (will be available for all .md and .html files as {{ my_dict.some_key }})
    some_key2: "mi valor personalizado en español"
  my_list:
    # available to iterate with {% for item in my_list %} {{ item }} {% endfor %}
    - "my custom value in english" (will be available for all .md and .html files as {{ my_list.0 }})
    - "mi valor personalizado en español"
  my_list_of_dicts:
    # available to iterate with {% for k, v in my_list_of_dicts %} {{ k }}: {{ v }} {% endfor %}
    - some_key: "my custom value in english"
    - some_key2: "mi valor personalizado en español"
```

### Define the site structure

The `nav` setting is the main configuration for the site structure.  
You need to add a sub-section for each language (`nav-en`, `nav-es`, etc).  

Inside the `page/docs` folder you need to create (if not exists) a folder
for each language (`docs-en`, `docs-es`, etc).  
For all languages, an `index.md` file is required.  

Inside each language folder you need to create (if not exists) the same
files described in the `nav-LANG` setting.  

### Custom site styles and javascript

If you need custom CSS styles, you can add them to the `page/assets/css/custom.css` file.  
If you need custom javascript, you can add them to the `page/assets/js/app.js` file.  

### Other static resources

If you need other static resources (like images), you can add them to the `page/assets` folder and they will be availabe
at `{{ assets_folder }}` in your template/markdown files (they are several examples available in the test templates).  

For example `<img src="{{ assets_folder }}/img/cordoba-rio.jpg"/>` or
`![cba river]({{ assets_folder }}/img/cordoba-rio.jpg)`.  

**Note**: If you plan to use resource file that contains spaces,
you'll need to use angle brackets.  
For example`![some pdf](<{{ assets_folder }}/img/spaced file name.pdf"/>)`.  
(note the angle brackets inside the URL).  

### Prepare your site

Prepare your internal custom settings for each language and prepare the environment

```bash
python3 okf_collab_docs/run.py build-config
```

For a list of common errors building your site, see [here](docs/build-errors.md).  

This process will create files and folders:
 - All the `conf/mkdocs-LANG.yml` required files (you don't need to touch them)
 - All the `page/docs/fixed-docs-LANG` required folder with an updated version of your MD files
 - Copy all assets to the `site` folder.

You don't need to touch any of this resources. They are _.gitignored_ and will be used to build the site.  

If this process succeeds, then **you're ready to deploy your site to GitHub Pages**, simply push your changes to GitHub.  
You can check the build process at the _Actions_ tab (https://github.com/USER/REPO-NAME/actions).  
Once the GitHub action finished, you'll need to enable github pages at https://github.com/USER/REPO-NAME/settings/page
and select the `gh-pages` branch.  

![gh pages](/docs/imgs/gh-pages.png)

After some minutes (GitHub will process your static site), your site will be available at https://USER.github.io/REPO-NAME  

#### Build your local site

You can also test you site locally and skip waiting for each GitHub action to finish.  
You can do this by builing the site locally and serving it with a local server.  

```
python3 okf_collab_docs/run.py build-local-site
```

... and serve the site locally

```
python3 okf_collab_docs/run.py serve
```

You'll see `serving at http://localhost:8033` and your local site is now redy to test with
all the languages you defined.  
**Note**: If you have a `Port in use` error, you can call
`python3 okf_collab_docs/run.py serve -p 8034` to use a different port.  

### PDF version

A PDF version for each language is generated automatically and it will be available at:
 - English version: `/pdf/doc-en.pdf`
 - Other languages: `/LANG/pdf/doc-LANG.pdf`

The URL for the PDF version is available in the `{{ pdf_url }}` variable in the template files.  
A _nav_ link pointing this URL will be added automatically at the end of each language site menu.  

The `/page/pdf/pdf-template-LANG` folder include custom styles,
cover and back cover templates for each language.  
[If you know what you're doing](https://github.com/orzih/mkdocs-with-pdf/blob/master/README.md#sample-pdf_event_hookpy-or-pdf_event_hook__init__py),
you can modify the `/pdf_event_hook.py` file.  

## More docs

More info about this project:

 - General notes: [docs/general-notes.md](docs/general-notes.md)
 - [Update latest changes from original template](docs/re-sync.md)
