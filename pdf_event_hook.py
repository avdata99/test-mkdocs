"""

Advanced Rendering Hooks (Experimental)
You can hook the PDF rendering process by creating a pdf_event_hook.py
(or pdf_event_hook/__init__.py) in your working directory.

"""

# import logging
# from mkdocs.structure.pages import Page


# def inject_link(
#     html: str,
#     href: str,
#     page: Page,
#     logger: logging
# ) -> str:
#     logger.info('(hook on inject_link)')
#     return html


# def pre_js_render(soup: BeautifulSoup, logger: logging) -> BeautifulSoup:
#     logger.info('(hook on pre_js_render)')
#     return soup


# def pre_pdf_render(soup: BeautifulSoup, logger: logging) -> BeautifulSoup:
#     logger.info('(hook on pre_pdf_render)')
#     tag = soup.find(lambda tag: tag.name ==
#                     'body' and 'data-md-color-scheme' in tag.attrs)
#     if tag:
#         tag['data-md-color-scheme'] = 'print'
#     return soup