from fasthtml.common import *

# Define the bootstrap version, style, and icon packs
cdn = 'https://cdn.jsdelivr.net/npm/bootstrap'
bootstrap_links = [
    Link(href=cdn+"@5.3.3/dist/css/bootstrap.min.css", rel="stylesheet"),
    Script(src=cdn+"@5.3.3/dist/js/bootstrap.bundle.min.js"),
    Link(href=cdn+"-icons@1.11.3/font/bootstrap-icons.min.css", rel="stylesheet")
]

# Attempt to avoid needing to use a .css file. Insert overrides here
css = Style('')

# Define the sidebar items
def SidebarItem(text, hx_get, hx_target, **kwargs):
    return Div(
        I(cls=f'bi bi-{text}'),
        Span(text),
        hx_get=hx_get, hx_target=hx_target,
        data_bs_parent='#sidebar', role='button',
        cls='list-group-item border-end-0 d-inline-block text-truncate',
        **kwargs)

# Define the sidebar
def Sidebar(sidebar_items, hx_get, hx_target):
    return Div(
        Div(*(SidebarItem(o, f"{hx_get}?menu={o}", hx_target) for o in sidebar_items),
            id='sidebar-nav',
            cls='list-group border-0 rounded-0 text-sm-start min-vh-100'
        ),
        id='sidebar',
        cls='collapse collapse-horizontal show border-end')

# Add remove buttons to the sidebar
sidebar_items = ('WebUI', 'Sunshine WebUI', 'Logs')

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

# The Log Page content is defined here
# Todo seperate the page into a different file
def logs_content():
    logs_dir = "/home/default/.cache/log"
    log_files = [f for f in os.listdir(logs_dir) if os.path.isfile(os.path.join(logs_dir, f)) and f.endswith('.log')]
    
    sorted_log_files = sorted(log_files)

    divs = []
    for log_file in sorted_log_files:
        file_path = os.path.join(logs_dir, log_file)
        with open(file_path, 'r') as file:
            lines = file.readlines()[-50:]
            content = "".join(lines)
            divs.append(Details(Summary(log_file), Pre(P(content)), cls="card mb-2"))
    
    return Div(*divs, cls='container-fluid py-5') if divs else Div("No log files found.")

# Define the routes for the application
# The Main route and layout when visiting the UI
@rt('/')
def get():
    return Div(
        Div(
            Div(
                Sidebar(sidebar_items, hx_get='menucontent', hx_target='#current-menu-content'),
                cls='col-auto px-0'),
            Main(
                A(I(cls='bi bi-list bi-lg py-2 p-1'),
                  href='#', data_bs_target='#sidebar', data_bs_toggle='collapse', aria_expanded='false', aria_controls='sidebar',
                  cls='border rounded-3 p-1 text-decoration-none bg-dark text-white bg-opacity-25 position-fixed my-1'),
                Div(
                  Div(
                    Div(
                    H1("Welcome to Steam Headless!", cls="py-5"),
                    P("Select an Item to get started"),
                    id="current-menu-content", style="width: 100%; height: 100vh;"),
                    cls='col-12'
                ), cls='row'),
                cls='col gx-0'),
            cls='row flex-nowrap'),
        cls='container-fluid')

# The route for the menu content, which is dynamically loaded via htmx into current-menu-content
@rt('/menucontent')
def menucontent(menu: str):

    current_ip="192.168.100.131" # FIXME cors x-headers something blocking iframe access from localhost?
    # current_ip="localhost"

    switch_cases = {
        'WebUI': f'<iframe src="http://{current_ip}:8083" width="100%" height="100%" style="border:none;" allow-insecure allowfullscreen></iframe>',
        'Sunshine WebUI': f'<iframe src="https://{current_ip}:47990" width="100%" height="100%" style="border:none;" allow-insecure allowfullscreen></iframe>',
        'Logs': logs_content()
    }

    return switch_cases.get(menu, Div("No content available"))

# Serve the application at port 8082
serve(port=8082)
