from fasthtml.common import *
#import requests

# Define the bootstrap version, style, and icon packs
cdn = 'https://cdn.jsdelivr.net/npm/bootstrap'
bootstrap_links = [
    Link(href=cdn+"@5.3.3/dist/css/bootstrap.min.css", rel="stylesheet"),
    Script(src=cdn+"@5.3.3/dist/js/bootstrap.bundle.min.js"),
    Link(href=cdn+"-icons@1.11.3/font/bootstrap-icons.min.css", rel="stylesheet"),
    Link(href=cdn+"about:blank", rel="shortcut icon") # Suppress favicon warning
]

# Attempt to avoid needing to use a .css file. Insert overrides here
css = Style()

# Page Element Contents and Structure
#

# Define the sidebar items
def SidebarItem(text, hx_get, hx_vals, hx_target, **kwargs):
    return Div(
        I(cls=f'bi bi-{text}'),
        Span(text),
        hx_get=hx_get, hx_vals=hx_vals, hx_target=hx_target,
        data_bs_parent='#sidebar', role='button',
        cls='list-group-item border-end-0 d-inline-block text-truncate',
        **kwargs)

# Define the sidebar
def Sidebar(sidebar_items, hx_get, hx_vals, hx_target):
    return Div(
        Div(*(SidebarItem(o, f"{hx_get}?menu={o}", hx_vals, hx_target) for o in sidebar_items),
            id='sidebar-nav',
            cls='list-group border-0 rounded-0 text-sm-start min-vh-100'
        ),
        id='sidebar',
        cls='collapse collapse-horizontal show border-end')

# Add remove buttons to the sidebar
sidebar_items = ('NoVNC', 'Sunshine', 'Logs', 'FAQ')

# The Log Page content is defined here
def logs_content():
    logs_dir = "/home/default/.cache/log"
    if os.path.isdir(logs_dir):
        # List all log files in the logs directory
        log_files = [f for f in os.listdir(logs_dir) if os.path.isfile(os.path.join(logs_dir, f)) and f.endswith('.log')]
        sorted_log_files = sorted(log_files)
        # Read the last 50 lines of each log file
        divs = []
        for log_file in sorted_log_files:
            file_path = os.path.join(logs_dir, log_file)
            with open(file_path, 'r') as file:
                lines = file.readlines()[-50:]
                content = "".join(lines)
                divs.append(Details(Summary(log_file), Pre(P(content)), cls="card mb-2"))
        # Return a container with all the logs using bootstrap classes
        return Div(*divs, cls='container-fluid py-5') if divs else Div("No log files found.")
    else:
        return Div("No log Directory Created.")

# The Faq Page content is defined here
# TODO add a proper FAQ page with markdown, styling, and links to the documentation
# def faq_content():
#     url = "https://raw.githubusercontent.com/Steam-Headless/docker-steam-headless/refs/heads/master/docs/troubleshooting.md"
#     response = requests.get(url)
#     if response.status_code == 200:
#         _content = response.text
#     else:
#         _content = "Failed to load content."

#     return Div(
#         H1("FAQ", cls="py-5"),
#         Pre(_content)
#     )

# Invokation of the fast_app function
# Define the main fastHTML app
app,rt = fast_app(
    pico=False, # Avoid conflicts between bootstrap styling and the built in picolink
    hdrs=(
        Meta(http_equiv='referrer', content='no-referrer'),
        Meta(http_equiv='Content-Security-Policy', content="frame-src 'self' *"),
        Meta(http_equiv='Access-Control-Allow-Origin', content="*"),
        bootstrap_links, 
        css)
)

# Define the routes for the application
# The Main route and responses to GET/POST requests
@rt('/')
def get():
    return Div(
        Div(
            Div(
                Sidebar(sidebar_items, hx_get='menucontent', hx_vals='js:{"myIP": window.location.hostname}', hx_target='#current-menu-content'),
                cls='col-auto px-0'),
            Main(
                A(I(cls='bi bi-controller bi-lg py-2 p-1'),
                  href='#', data_bs_target='#sidebar', data_bs_toggle='collapse', aria_expanded='false', aria_controls='sidebar',
                  cls='border rounded-3 p-1 text-decoration-none bg-dark text-white bg-opacity-25 position-fixed my-1'),
                Div(
                  Div(
                    Div(
                    H1("Welcome to Steam Headless!", cls="py-5"),
                    P("Select an Item to get started"),
                    id="current-menu-content", style="width: 100%; height: 100vh;"),
                    cls='col-12'
                ), cls='row gx-0'),
                cls='col gx-0 overflow-hidden'),
            cls='row flex-nowrap'),
        cls='container-fluid')

# The route for the menu content, which is dynamically loaded via htmx into #current-menu-content
@rt('/menucontent')
def menucontent(menu: str, myIP: str):

    switch_cases = {
        'NoVNC': f'<iframe id="desktopUI" src="http://{myIP}:8083" width="100%" height="100%" style="border:none;" allow-insecure allowfullscreen></iframe>',
        'Sunshine': f'<iframe id="sunshineUI" src="https://{myIP}:47990" width="100%" height="100%" style="border:none;" allow-insecure allowfullscreen></iframe>',
        'Logs': logs_content(),
        #'FAQ': faq_content()
    }

    return switch_cases.get(menu, Div("No content available"))

# Run the app
# Serve the application at port 8082
serve(port=8082)
