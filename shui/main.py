from fasthtml.common import *
from PIL import Image, ImageDraw, ImageFont
import requests
import json
import os
import socket

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
css = Style()

class Game:
    game_id:int; game_name:str; game_added:bool
    def __ft__(self):
        return Li(
            Div(
                Strong(self.game_name, cls='col-auto'),
                Div(
                    Button(
                        'Add To Sunshine', hx_get=f'/add/{self.game_id}', target_id=f'appid-{self.game_id}',
                        cls='btn btn-primary me-2'
                    ),
                    Button(
                        'Remove', hx_get=f'/remove/{self.game_id}', target_id=f'appid-{self.game_id}',
                        cls='btn btn-danger me-2'
                    ),
                    Strong(
                        I(cls='bi bi-toggle-on') if self.game_added else I(cls='bi bi-toggle-off'),
                        id=f'appid-{self.game_id}'
                    ), cls='col d-flex justify-content-end'
                ), cls='row'
            ), cls='list-group-item'
        )
class Setting:
    key:str; value:str
    def __ft__(self):
        return Li(
            Strong(self.key, cls='col-auto'),
            Input(placeholder=f"{self.value}", id=f'setVal-{self.key}', cls='col-8'),
            Button('Save', hx_post=f'/save/{self.key}', cls='btn btn-danger col-1'),
            cls='list-group-item grid'
        )
class Logfile:
    def __init__(self, filename: str, content: str):
        self.filename = filename
        self.content = content
    def __ft__(self):
        return Details(Summary(self.filename), Pre(P(self.content)), cls='card mb-2')

# # Define the database and create tables
# if not os.path.isfile('/home/default/.cache/shui.db'):
#     db = database('/home/default/.cache/shui.db')
#     gamedb = db.create(Game, pk='game_id')
#     settingdb = db.create(Setting, pk='key')
#     settingdb.insert(
#         Setting(
#             key='Poster Directory',
#             value='/home/default/.local/share/posters'
#         )
#     )
# else:
#     db = database('/home/default/.cache/shui.db')
#     gamedb = db.table(Game, pk='game_id')
#     settingdb = db.table(Setting, pk='key')

# Define the database and create tables
db = database('/home/default/.cache/shui.db')
gamedb = db.create(Game, pk='game_id')
settingdb = db.create(Setting, pk='key')

# Get the Server IP Address
def get_local_ip():
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Connect to an external server (doesn't actually send any data)
        s.connect(("8.8.8.8", 80))

        # Get the local IP address
        local_ip = s.getsockname()[0]

        # Close the socket
        s.close()

        return local_ip
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Use the function to get the server IP
server_ip = get_local_ip()

# Grab Any ENV variables for later use
port_novnc_web = os.getenv('PORT_NOVNC_WEB')

# Setup toast notification system
def notify(header, message, duration=500, **kwargs):
    return Div(
        Div(
            Div(
                Strong(header, cls='me-auto'),
                Button('Close', cls='btn-close', data_bs_dismiss='toast'),
                cls='toast-header'
            ),
            Div(
                P(message),
                cls='toast-body'
            ), id='liveToast', cls='toast', role='alert'
        ), cls='toast-container position-fixed bottom-0 end-0 p-3', style='z-index: 11', data_bs_delay=duration, data_bs_autohide='true'
    ), Script('var toastEl = document.getElementById("liveToast"); var toast = bootstrap.Toast.getOrCreateInstance(toastEl); toast.show();')

# Define the sidebar items
def SidebarItem(text, hx_get, hx_target, **kwargs):
    return Div(
        I(cls=f'bi bi-{text}'),
        Span(text),
        hx_get=hx_get, hx_target=hx_target,
        data_bs_toggle='modal', data_bs_target="#centeredScrollableModal",
        data_bs_parent='#sidebar', data_bs_dismiss='offcanvas', role='button',
        cls='list-group-item border-end-0 d-inline-block text-truncate',
        **kwargs)

# Define the sidebar
def Sidebar(sidebar_items, hx_get, hx_target):
    return Div(
        Div(*(SidebarItem(o, f"{hx_get}?menu={o}", hx_target) for o in sidebar_items),
            id='sidebar-nav',
            cls='list-group border-0 rounded-0 text-sm-start'
        ),
        id='sidebar',
        cls='offcanvas offcanvas-start w-25')

# Add remove buttons to the sidebar
sidebar_items = ('App Manager', 'Logs', 'FAQ')

# The Log Page content is defined here
def logs_content():
    logs_dir = "/home/default/.cache/log"
    if os.path.isdir(logs_dir):
        # List all log files in the logs directory
        log_files = [f for f in os.listdir(logs_dir) if os.path.isfile(os.path.join(logs_dir, f)) and f.endswith('.log')]
        sorted_log_files = sorted(log_files)
        # Read the last 50 lines of each log file
        logfiles = []
        for log_file in sorted_log_files:
            file_path = os.path.join(logs_dir, log_file)
            with open(file_path, 'r') as file:
                lines = file.readlines()[-50:]
                content = "".join(lines)
                logfiles.append(Logfile(log_file, content))
        # Return a container with all the logs using bootstrap classes
        return Div(*logfiles, cls='container py-5') if logfiles else Div("No log files found.")
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
def settings_content():
    return Div(
        Ul(*settingdb(), id='settings-ul', cls='list-group'),
            cls='container py-5'
    )

# Sunshine App Manager content is defined here
def sunshine_appmanager_content():
    return Div(
        Div(
            H2("Sunshine Manager", cls='col-10')
        ), 
        Div(
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
            Div(
                Ul(*gamedb(order_by='-game_added'), id='game-ul', cls='list-group'),
                cls='row py-2'
            )
        ), cls='container py-5'
    )

# Invokation of the fast_app function
# Define the main fastHTML app
app,rt = fast_app(
    pico=False, # Avoid conflicts between bootstrap styling and the built in picolink
    hdrs=(
        bootstrap_links, 
        css)
)

def get_steam_library_folders():
    library_folders = []
    
    with open('/home/default/.steam/steam/steamapps/libraryfolders.vdf', 'r') as file:
        content = file.read()
    
    # Use regex to find all paths
    path_pattern = r'"path"\s*"([^"]*)"'
    paths = re.findall(path_pattern, content)
    
    # Append 'steamapps' to each path
    for path in paths:
        full_path = os.path.join(path, 'steamapps')
        library_folders.append(full_path)
    
    return library_folders

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
                    # Get the parent in case its a DLC
                    parent_appid_match = re.search(r'"parentappid"\s+"(\d+)"', acf_content)
                    if parent_appid_match:
                        parent_appid = int(parent_appid_match.group(1))
                        found_appids.add(parent_appid) 
                        
                        # Check if the parent game already exists in the database
                        if parent_appid not in gamedb:
                            game_name_match = re.search(r'"name"\s+"([^"]+)"', acf_content)
                            if game_name_match:
                                game_name = game_name_match.group(1)
                                gamedb.insert(Game(
                                    game_id=parent_appid,
                                    game_name=game_name,
                                    game_added=False
                                ))
                    else:
                        # If no parent appid
                        found_appids.add(appid) 
                        
                        # Check if the game already exists in the database
                        if appid not in gamedb:
                            game_name_match = re.search(r'"name"\s+"([^"]+)"', acf_content)
                            if game_name_match:
                                game_name = game_name_match.group(1)
                                gamedb.insert(Game(
                                    game_id=appid,
                                    game_name=game_name,
                                    game_added=False
                                ))
    # TODO Remove any appids from gamedb that were not found in the ACF files
    

# Functions to manipulate the sunshine apps.json file
# TODO make this more robust and add error handling
def add_sunshine_app(app_name, app_id, conf_loc='/home/default/.config/sunshine/apps.json'):

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

    fetch_and_resize_poster(app_id, app_name)

    with open(conf_loc, 'w') as f:
        json.dump(data, f, indent=4)

# Function to delete a Sunshine App from the apps.json file
def del_sunshine_app(app_name, app_id, conf_loc='/home/default/.config/sunshine/apps.json'):

    with open(conf_loc, 'r', encoding='utf-8') as f:
        data = json.load(f) 
    
    # Filter out the app with the specified name? maybe a better way?
    data['apps'] = [app for app in data['apps'] if app['name'] != app_name] 

    with open(conf_loc, 'w') as f:
        json.dump(data, f, indent=4)

# Function to fetch and resize Steam game posters
# TODO Center text on the image if no header image is found
def fetch_and_resize_poster(game_id, game_name, save_directory='/home/default/.local/share/posters'):
    # Create the directory if it doesn't exist
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    
    # Check if the image already exists to avoid overwriting
    if not os.path.exists(os.path.join(save_directory, f'{game_id}.png')):
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
# The Main route
@rt('/')
def get():
    return Main(
        Sidebar(
            sidebar_items, hx_get='menucontent', hx_target='#current-menu-content'
        ),
        A(
            I(cls='bi bi-controller bi-lg py-2 p-1'),
            href='#', data_bs_target='#sidebar', data_bs_toggle='offcanvas', aria_expanded='false', aria_controls='sidebar',
            cls='border rounded-3 p-1 text-decoration-none bg-dark text-white bg-opacity-25 position-fixed my-2 mx-2'
        ),
        Iframe(
            id='landing', src=f'http://{server_ip}:{port_novnc_web}/web/index.html?autoconnect=true',
            style='width: 100%; height: 100vh; border:none; overflow-y:hidden;'
        ),
        Div(
            Div(
                Div(
                    Div(id='current-menu-content', cls='modal-body'),
                    cls='modal-content'
                ),
                cls='modal-dialog modal-xl modal-dialog-centered modal-dialog-scrollable'
            ),
            id="centeredScrollableModal", cls='modal', tabindex='-1', aria_labelledby='modalLabel', aria_hidden='true'
        )
    )

# The route for the menu content, which is dynamically loaded via htmx into #current-menu-content
@rt('/menucontent')
def menucontent(menu: str):
    switch_cases = {
        #'Installers':  installer_content(),
        'App Manager': sunshine_appmanager_content(),
        'Logs': logs_content(),
        'FAQ': faq_content()
        #'Settings': settings_content()
    }

    return switch_cases.get(menu, Div("No content available", cls='py-5'))

# Routes for the Sunshine App Manager
# The route to reload the app manager content
@rt('/reload')
def post():
    get_installed_steam_games('/mnt/games/SteamLibrary/steamapps')
    return Script('window.location.href = "/"')

# Function to restart sunshine
# TODO Fix Not authorized error in sunshine's logs
@rt('/sunshine-restart')
def post():
    #username = "sunshine"
    #password = "sunshine"
    # Encode credentials for Basic Authentication
    #credentials = f"{username}:{password}"
    #encoded_credentials = base64.b64encode(credentials.encode())

    api_url = f"https://{server_ip}:47990/api/restart"  
 
    headers = {
        #"Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/json"
    }

    # Send the restart request
    response = requests.post(api_url, headers=headers, verify=False)

    if response.status_code == 200:
        return notify("Sunshine Manager", "Restarting Sunshine", 1000)
    else:
        return notify("Sunshine Manager", "Failed to Restart Sunshine", 1000)
    

# The route to remove a game from sunshine
@rt('/remove/{game_id}')
def get(game_id:int):
    game = gamedb[game_id]
    game.game_added = False
    gamedb.update(game)
    del_sunshine_app(game.game_name, game.game_id)
    return I(hxswap="innerHTML", cls='bi bi-toggle-off')

# The route to add a game to sunshine
@rt('/add/{game_id}')
def get(game_id:int):
    game = gamedb[game_id]
    game.game_added = True
    gamedb.update(game)
    add_sunshine_app(game.game_name, game.game_id)
    return I(hxswap="innerHTML", cls='bi bi-toggle-on')

# Run the app
# Serve the application at port 8082
serve(port=8082, reload=False)