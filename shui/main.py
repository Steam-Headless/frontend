from fasthtml.common import *
#from pyxtermjs import XTermApp
import requests
import json
import os

# Define the bootstrap version, style, and icon packs
cdn = 'https://cdn.jsdelivr.net/npm/bootstrap'
bootstrap_links = [
    Link(href=cdn+"@5.3.3/dist/css/bootstrap.min.css", rel="stylesheet"),
    Script(src=cdn+"@5.3.3/dist/js/bootstrap.bundle.min.js"),
    Link(href=cdn+"-icons@1.11.3/font/bootstrap-icons.min.css", rel="stylesheet"),
    #Link(rel='stylesheet', href='node_modules/@xterm/xterm/css/xterm.css'), # Include xterm styles
    #Script(src='node_modules/@xterm/xterm/lib/xterm.js'), # Include xterm styles
    Link(href=cdn+"about:blank", rel="shortcut icon") # Suppress favicon warning
]

# Attempt to avoid needing to use a .css file. Insert overrides here
css = Style()

# Page Element Contents and Structure
#

## Define how to desiplay/render items for the gamedb default table
## Todo fix rendering to display the items in a more user friendly way
def render(game):
    return Li(
        Div(
            Strong(
                game.game_name,
                cls='col-auto',
            ),
            Div(
                Button(
                    'Add To Sunshine', hx_get=f'/add/{game.game_id}', target_id=f'appid-{game.game_id}',
                    cls='btn btn-primary me-2'
                ),
                Button(
                    'Remove', hx_get=f'/remove/{game.game_id}', target_id=f'appid-{game.game_id}',
                    cls='btn btn-danger me-2'
                ),
                Strong(
                    I(cls='bi bi-toggle-on') if game.game_added else I(cls='bi bi-toggle-off'),
                    id=f'appid-{game.game_id}'
                ),
                cls='col d-flex justify-content-end'
            ),
            cls='row'
        ),
        cls='list-group-item',
    )

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
sidebar_items = ('Desktop', 'Sunshine', 'Shell', 'Installers', 'App Manager', 'Logs', 'FAQ')

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
def faq_content():
    url = "https://raw.githubusercontent.com/Steam-Headless/docker-steam-headless/refs/heads/master/docs/troubleshooting.md"
    response = requests.get(url)
    if response.status_code == 200:
        _content = response.text
    else:
        _content = "Failed to load content."

    return Div(
        H1("FAQ", cls="py-5"),
        Pre(_content),
        cls="container"
    )

# A interactive SHELL is spawed here
def terminal_content():
    return Div(
        Div(id='terminal', cls="py-5"),
        Script("var term = new Terminal(); term.open(document.getElementById('terminal'));")
    )

# The installer page content is defined here
# TODO figure out the best way to handle installers
def installer_content():
    return Div(
        H1("Installers", cls="py-5"),
        cls="container"
    )

# Sunshine App Manager content is defined here
def sunshine_appmanager_content():
    return Div(
        H1("Sunshine Manager"),
        cls='container py-5'
    ), Div(
        Br(),
        Button("Reload Steam Games",
            hx_post="/reload",
            cls='container-fluid btn btn-primary'
        ),
        Br(),
        Script('''
            function filterList() { 
                var input, filter, ul, li, i, txtValue; 
                input = document.getElementById(\'filter-games\'); 
                filter = input.value.toLowerCase(); 
                ul = document.getElementById("game-ul"); 
                li = ul.getElementsByTagName(\'li\'); 
                for (i = 0; i < li.length; i++) { 
                    txtValue = li[i].textContent || li[i].innerText; if (txtValue.toLowerCase().indexOf(filter) > -1) { li[i].style.display = ""; } else { li[i].style.display = "none"; } 
                } 
            }
        '''),
        Input(id="filter-games", onkeyup="filterList()", placeholder="Type to filter list", cls='container-fluid form-control'),
        Div (
            Ul(*gamedb(order_by='-game_added'), id='game-ul', cls='list-group'),
            cls='row py-2'
        )
    )

# Invokation of the fast_app function
# Define the main fastHTML app
app,rt,gamedb,Game = fast_app('/home/default/.cache/gamedb.db',
    render=render,
    game_id=int,
    game_name=str,
    game_added=bool,
    pk='game_id',
    pico=False, # Avoid conflicts between bootstrap styling and the built in picolink
    hdrs=(
        #Meta(http_equiv='referrer', content='no-referrer'),
        #Meta(http_equiv='Content-Security-Policy', content="frame-src 'self' *"),
        #Meta(http_equiv='Content-Security-Policy', content="upgrade-insecure-requests"),
        #Meta(http_equiv='Access-Control-Allow-Origin', content="*"),
        bootstrap_links, 
        css)
)

# Function to populate the sqlite db with steam game data
# TODO load the sqlite db into games and add/remove games from the db based on steam directory changes
def get_installed_steam_games(steam_dir):
    for filename in os.listdir(steam_dir):
        if filename.endswith('.acf'):
            acf_file = os.path.join(steam_dir, filename)
            with open(acf_file, 'r', encoding='utf-8') as f:
                acf_content = f.read()
                appid_match = re.search(r'"appid"\s+"(\d+)"', acf_content)

                if appid_match:
                    appid = int(appid_match.group(1))
                    game_name_match = re.search(r'"name"\s+"([^"]+)"', acf_content)
                    if game_name_match:
                        game_name = game_name_match.group(1)
                        if appid in gamedb:
                            continue
                        else:
                            gamedb.insert(Game(
                                game_id=appid,
                                game_name=game_name,
                                game_added=False
                            ))

# Functions to manipulate the sunshine apps.json file
# TODO change functionality to add/remove apps from the sunshine config file using the appid
def add_sunshine_app(**kwargs):
    app_name = kwargs['app_name']
    app_id = kwargs['app_id']
    conf_loc = kwargs['conf_loc']
    with open(filename, 'r', encoding='utf-8') as f:
        data = load_apps_from_file(conf_loc)

    new_app = {
        "name": "{app_name}",
        "output": "SH-run.txt",
        "detached": [
            "/usr/bin/sunshine-run /usr/games/steam steam://rungameid/{app_id}"
        ],
        "exclude-global-prep-cmd": "True",
        "elevated": "False",
         "prep-cmd": [
            {
                "do": "/usr/bin/xfce4-minimise-all-windows",
                "undo": "/usr/bin/sunshine-stop"
            },
            {
                "do": "",
                "undo": "/usr/bin/xfce4-close-all-windows"
            }
        ],
        "image-path": "/home/default/.local/share/posters/{app_id}.png",
        "working-dir": "/home/default"
    }

    data['apps'].append(new_app)
    updated_json_data = json.dumps(data, indent=4)

    with open(conf_loc, 'w') as json_file:
        json_file.write(updated_json_data)

def del_sunshine_app(**kwargs):
    app_name = kwargs['app_name']
    app_id = kwargs['app_id']
    conf_loc = kwargs['conf_loc']
    with open(filename, 'r', encoding='utf-8') as f:
        data = load_apps_from_file(conf_loc)
    
    # Filter out the app with the specified name? maybe a better way?
    data['apps'] = [app for app in data['apps'] if app['name'] != app_name] 
    
    updated_json_data = json.dumps(data, indent=4)

    with open(conf_loc, 'w') as json_file:
        json_file.write(updated_json_data)

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
                  cls='border rounded-3 p-1 text-decoration-none bg-dark text-white bg-opacity-25 position-fixed my-2 mx-2'),
                Div(
                  Div(
                    Div(
                    # TODO Make a nice landing page with a nice logo and some info about the project
                    H1("Welcome to Steam Headless!", cls="py-5 mx-2"),
                    P("Select an Item to get started", cls="mx-2"),
                    id="current-menu-content", style="width: 100%; height: 100vh;"),
                    # NOTE End of landing page section
                    cls='col-12'
                ), cls='row gx-0'),
                cls='col gx-0 overflow-hidden'),
            cls='row flex-nowrap'),
        cls='container-fluid')

# The route for the menu content, which is dynamically loaded via htmx into #current-menu-content
@rt('/menucontent')
def menucontent(menu: str, myIP: str):

    switch_cases = {
        'Desktop': f'<iframe id="desktopUI" src="http://{myIP}:8083/web/index.html?autoconnect=true" width="100%" height="100%" style="border:none;" allow-insecure allowfullscreen></iframe>',
        'Sunshine': f'<iframe id="sunshineUI" src="https://{myIP}:47990" width="100%" height="100%" style="border:none;" allow-insecure allowfullscreen></iframe>',
        #'Shell': terminal_content(),
        #'Installers':  installer_content(),
        'App Manager': sunshine_appmanager_content(),
        'Logs': logs_content(),
        'FAQ': faq_content()
    }

    return switch_cases.get(menu, Div("No content available", cls='py-5'))

# Routes for the Sunshine App Manager
# The route to reload the app manager content
@rt('/reload')
def post():
    get_installed_steam_games('/mnt/games/SteamLibrary/steamapps')

# The route to remove a game from sunshine
@rt('/remove/{game_id}')
def get(game_id:int):
    # TODO actually remove the game instead of toggeling the boolean in the db
    game = gamedb[game_id]
    game.game_added = False
    gamedb.update(game)
    #add_sunshine_app(app_name=game.game_name, app_id=game.app_id, conf_loc='/home/default/.config/sunshine/apps.json')
    return I(hxswap="innerHTML", cls='bi bi-toggle-off')

# The route to add a game to sunshine
@rt('/add/{game_id}')
def get(game_id:int):
    # TODO actually add the game instead of toggeling the boolean in the db
    game = gamedb[game_id]
    game.game_added = True
    gamedb.update(game)
    #del_sunshine_app(app_name=game.game_name, app_id=game.app_id, conf_loc='/home/default/.config/sunshine/apps.json')
    return I(hxswap="innerHTML", cls='bi bi-toggle-on')

# Run the app
# Serve the application at port 8082
serve(port=8082)
