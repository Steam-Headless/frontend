from fasthtml.common import *
from PIL import Image, ImageDraw, ImageFont
import requests
import json
import os

# Define the bootstrap version, style, and icon packs
cdn = 'https://cdn.jsdelivr.net/npm/bootstrap'
bootstrap_links = [
    Link(href=cdn+"@5.3.3/dist/css/bootstrap.min.css", rel="stylesheet"),
    Script(src=cdn+"@5.3.3/dist/js/bootstrap.bundle.min.js"),
    Link(href=cdn+"-icons@1.11.3/font/bootstrap-icons.min.css", rel="stylesheet"),
    Link(href=cdn+"about:blank", rel="shortcut icon") # Suppress favicon warning
]

# Attempt to avoid needing to use a .css file. Insert overrides here if needed
# Placeholders for menu elements
css = Style("""
.bi-Desktop {
}
.bi-Sunshine {
}
.bi-Settings {
}
.bi-Installers {
}
.bi-AppManager {
}
.bi-Logs {
}
.bi-FAQ {
}
""")

# Page Element Contents and Structure
#

## Define how to desiplay/render items for the gamedb default table
## Todo fix rendering to display the items in a more user friendly way
def render(game):
    return Li(
        Div(
            Strong(game.game_name, cls='col-auto'),
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
                ), cls='col d-flex justify-content-end'
            ), cls='row'), cls='list-group-item'
    )

# Setup toast notification system
# def notify(message, hx_target, duration=3000, **kwargs):
#     return Div(
#         Div(
#             Div(
#                 Strong('Toast Header Section', cls='me-auto'),
#                 Button('Close', cls='btn-close', data_bs_dismiss='toast'),
#                 cls='toast-header'
#             ),
#             Div(
#                 P(message),
#                 cls='toast-body'
#             ), id='liveToast', cls='toast', role='alert'
#         ), cls='toast-container position-fixed bottom-0 end-0 p-3', style='z-index: 11', data_bs_delay=duration, data_bs_autohide='true'
#     ), Script('var toastEl = document.getElementById("liveToast"); var toast = new bootstrap.Toast(toastEl); toast.show();')

# Define the sidebar items
def SidebarItem(text, hx_get, hx_vals, hx_target, **kwargs):
    return Div(
        I(cls=f'bi bi-{text}'),
        Span(text),
        hx_get=hx_get, hx_vals=hx_vals, hx_target=hx_target,
        data_bs_parent='#sidebar', data_bs_dismiss='offcanvas', role='button',
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
        cls='offcanvas offcanvas-start')

# Add remove buttons to the sidebar
sidebar_items = ('Desktop', 'Sunshine', 'Installers', 'App Manager', 'Logs', 'FAQ', 'Settings')

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

# The installer page content is defined here
# TODO figure out the best way to handle installers
def installer_content():
    return Div(
        H1("Installers", cls="py-5"),
        cls="container"
    )

# The settings page content is defined here
# TODO lots and lots
def settings_content():
    return Div(
        Ul(
            Li(
                Span("Steam Directory"),
                Input(
                    type="text", 
                    value="/mnt/games/SteamLibrary/steamapps", 
                    placeholder="/mnt/games/SteamLibrary/steamapps"
                ), cls='list-group-item'
            ),
            Li(
                Div(
                    Input("Enable Poster Generation", type="checkbox")
                ),
                Div(
                    Button("Download all Posters", cls='btn btn-primary me-2')
                ),
                Div(
                    Button("Delete Posters", cls='btn btn-danger me-2')
                )
            ), cls='list-group-item'
        ), cls="container py-5"
    )

# Sunshine App Manager content is defined here
def sunshine_appmanager_content():
    return Div(
        H2("Sunshine Manager", cls='col-10'),
        Button("Restart Sunshine",
            hx_post="/sunshine-restart",
            cls='col d-flex btn btn-danger'
        ), cls='container-fluid row py-5'
    ), Div(
        Button("Reload Steam Games",
            hx_post="/reload",
            cls='container-fluid btn btn-primary'
        ),
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
        # Div(
        #     Input(id="label", type="text", placeholder="Global Run Command:", readonly="", cls=''),
        #     Input(id="sunshine-pre", type="text", placeholder="/usr/bin/sunshine-run", cls='col-auto'),
        #     cls='inline-flex'
        # ),
        Div(
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
def get_installed_steam_games(steam_dir):
    found_appids = set()  # Use a set to store unique appids found

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
                        found_appids.add(appid)  # Add appid to the set of found appids
                        if appid in gamedb:
                            continue
                        else:
                            gamedb.append(Game(
                                game_id=appid,
                                game_name=game_name,
                                game_added=False
                            ))

    # Remove any appids from gamedb that were not found in the ACF files
    gamedb[:] = [game for game in gamedb if game.game_id in found_appids]

# Functions to manipulate the sunshine apps.json file
# TODO make this more robust and add error handling
def add_sunshine_app(**kwargs):
    app_name = kwargs['app_name']
    app_id = kwargs['app_id']
    conf_loc = kwargs['conf_loc']

    with open(conf_loc, 'r') as f:
        data = json.load(f)

    new_app = {
        "name": f"{app_name}",
        "output": "SH-run.txt",
        "detached": [
            f"/usr/bin/sunshine-run /usr/games/steam steam://rungameid/{app_id}"
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
        "image-path": f"/home/default/.local/share/posters/{app_id}.png",
        "working-dir": "/home/default"
    }

    data['apps'].append(new_app)

    #fetch_and_resize_poster(app_id, app_name)

    with open(conf_loc, 'w') as f:
        json.dump(data, f, indent=4)

# Function to delete a Sunshine App from the apps.json file
def del_sunshine_app(**kwargs):
    app_name = kwargs['app_name']
    app_id = kwargs['app_id']
    conf_loc = kwargs['conf_loc']
    with open(conf_loc, 'r', encoding='utf-8') as f:
        data = json.load(f) 
    
    # Filter out the app with the specified name? maybe a better way?
    data['apps'] = [app for app in data['apps'] if app['name'] != app_name] 

    with open(conf_loc, 'w') as f:
        json.dump(data, f, indent=4)

# Function to fetch and resize Steam game posters
# TODO switch to streamgriddb? can only find landscape images from steam
def fetch_and_resize_poster(game_id, game_name, save_directory='/home/default/.local/share/posters'):
    # Create the directory if it doesn't exist
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    
    # Create a blank image with black background
    image = Image.new('RGB', (600, 800), 'black')
    draw = ImageDraw.Draw(image)

    # Define the font and text size
    # Draw a Title to show that it is steam-headless managed
    font = ImageFont.truetype("arial.ttf", 40)
    draw.text((150, 20), "Steam Headless", fill='white', font=font)

    # Draw tha game name at the footer
    text_width = draw.textlength(str(game_name), font=font)
    name_x_offset = (image.width - text_width) / 2

    # Draw the text with wrapping if necessary
    lines = []
    words = game_name.split(' ')
    line = ''
    for word in words:
        test_line = line + word + ' '
        test_width = draw.textlength(test_line, font=font)
        if test_width <= image.width:
            line = test_line
        else:
            lines.append(line)
            line = word + ' '
    lines.append(line)

    # Calculate the y-coordinate for each line of text
    name_y_offset = 600  # Starting y-coordinate
    for i, line in enumerate(lines):
        name_x_offset = (image.width - draw.textlength(str(line), font=font)) / 2
        draw.text((name_x_offset, name_y_offset), line, fill='white', font=font)
        name_y_offset += 40

    # Check if the image already exists to avoid overwriting
    if not os.path.exists(os.path.join(save_directory, f'{game_id}.png')):
        # Fetch the game poster from Steam API
        url = f'https://store.steampowered.com/api/appdetails?appids={game_id}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if str(game_id) in data and data[str(game_id)]['success']:
                poster_url = data[str(game_id)]['data']['header_image']

                response_poster = requests.get(poster_url)
                if response_poster.status_code == 200:
                    # Open the fetched image and resize it to fit
                    poster_image = Image.open(requests.get(poster_url, stream=True).raw)
                    height = int((600 / poster_image.width) * poster_image.height)
                    resized_poster = poster_image.resize((600, height))
                    
                    # Calculate the position to center the image on the main image
                    x_offset = 0
                    y_offset = (800 - height) // 2
                    
                    # Paste the resized poster onto the black background
                    image.paste(resized_poster, (x_offset, y_offset))
        #TODO else use steamgridb here if api returns no image?
                
        # Save the final image appid.png
        image.save(f'{save_directory}/{game_id}.png')

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
                  href='#', data_bs_target='#sidebar', data_bs_toggle='offcanvas', aria_expanded='false', aria_controls='sidebar',
                  cls='border rounded-3 p-1 text-decoration-none bg-dark text-white bg-opacity-25 position-fixed my-2 mx-2'),
                Div(
                  Div(
                    Div(
                        # NOTE Start of the landing page section
                        Iframe(id='landing', src='', width='100%', height='100%', style='border:none', allowfullscreen=''),
                        Script('document.getElementById("landing").src = "http://" + window.location.hostname + ":8083/web/index.html?autoconnect=true";'),
                        id="current-menu-content", style="width: 100%; height: 100vh;"),
                        # NOTE End of landing page section
                    cls='col-12'
                ), cls='row gx-0'),
                cls='col gx-0 overflow-hidden'),
            Div(
                Div(
                    Div(cls='toast-header'),
                    Div(cls='toast-body'), id='liveToast', cls='toast', role='alert'
                ), id='toast-target', cls='toast-container position-fixed bottom-0 end-0 p-3', style='z-index: 11'
            ),
            cls='row flex-nowrap'),
        cls='container-fluid')

# The route for the menu content, which is dynamically loaded via htmx into #current-menu-content
@rt('/menucontent')
def menucontent(menu: str, myIP: str):

    switch_cases = {
        'Desktop': f'<iframe id="desktopUI" src="http://{myIP}:8083/web/index.html?autoconnect=true" width="100%" height="100%" style="border:none;" allowfullscreen></iframe>',
        'Sunshine': f'<iframe id="sunshineUI" src="https://{myIP}:47990" width="100%" height="100%" style="border:none;" allow-insecure allowfullscreen></iframe>',
        #'Installers':  installer_content(),
        'App Manager': sunshine_appmanager_content(),
        'Logs': logs_content(),
        'FAQ': faq_content(),
        'Settings': settings_content()
    }

    return switch_cases.get(menu, Div("No content available", cls='py-5'))

# Routes for the Sunshine App Manager
# The route to reload the app manager content
@rt('/reload')
def post():
    get_installed_steam_games('/mnt/games/SteamLibrary/steamapps')
    return Script('window.location.href = "/"')

# Function to restart sunshine
# TODO implement the actual restart logic & have the button show the status
# @rt('/sunshine-restart')
# def post():
#     notify('Test', hx_target='#toast-target', hxswap='innerHTML')
#     #curl -X POST https://<your_server_ip>:47990/api/restart -H "Authorization: Bearer <your_api_token>"
#     #curl -X GET https://<your_server_ip>:47990/api/status -H "Authorization: Bearer <your_api_token>"
    

# The route to remove a game from sunshine
@rt('/remove/{game_id}')
def get(game_id:int):
    game = gamedb[game_id]
    game.game_added = False
    gamedb.update(game)
    del_sunshine_app(app_name=game.game_name, app_id=game.game_id, conf_loc='/home/default/.config/sunshine/apps.json')
    return I(hxswap="innerHTML", cls='bi bi-toggle-off')

# The route to add a game to sunshine
@rt('/add/{game_id}')
def get(game_id:int):
    game = gamedb[game_id]
    game.game_added = True
    gamedb.update(game)
    add_sunshine_app(app_name=game.game_name, app_id=game.game_id, conf_loc='/home/default/.config/sunshine/apps.json')
    return I(hxswap="innerHTML", cls='bi bi-toggle-on')

# Run the app
# Serve the application at port 8082
serve(port=8082)