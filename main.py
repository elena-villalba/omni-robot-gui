from ForwardKinematics import ForwardKinematics
from InverseKinematics import InverseKinematics
from PathFollowing import PathFollowing
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import signal
import sys

class RobotSimGUI:
    def __init__(self):
        # Initialize instances of ForwardKinematics, InverseKinematics, and PathFollowing classes
        self.forward_kinematics_class = ForwardKinematics()
        self.inverse_knimatics_class = InverseKinematics()
        self.path_following_class = PathFollowing()

        self.init() # Initialize the GUI
    
    def init(self):
        self.root = tk.Tk() # Create the main window
        self.root.title("Simulation of a 3-Wheel Omnidirectional Robot") # Set window title
        self.root.attributes('-zoomed', True) # Maximize the window
        
        # Main frame to hold everything
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Initialize the main frame with buttons
        self.initial_frame = tk.Frame(self.main_frame)
        self.initial_frame.pack(fill=tk.BOTH, expand=True)

        # Center the main frame with buttons
        self.center_frame = tk.Frame(self.initial_frame)
        self.center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Create rounded button images
        self.button_image = self.create_rounded_rectangle_image(450, 100, 25, 'blue')
        self.button_image_hover = self.create_rounded_rectangle_image(450, 100, 25, 'lightblue')

        # Create buttons for different simulations
        self.direct_kin_button = tk.Label(self.center_frame, image=self.button_image, text="Forward Kinematics", compound="center", fg="white", font=('Helvetica', 24))
        self.direct_kin_button.bind("<Button-1>", lambda e: self.forward_kinematics())
        self.direct_kin_button.bind("<Enter>", lambda e: self.direct_kin_button.config(image=self.button_image_hover))
        self.direct_kin_button.bind("<Leave>", lambda e: self.direct_kin_button.config(image=self.button_image))
        self.direct_kin_button.pack(pady=30)

        self.inverse_kin_button = tk.Label(self.center_frame, image=self.button_image, text="Inverse Kinematics", compound="center", fg="white", font=('Helvetica', 24))
        self.inverse_kin_button.bind("<Button-1>", lambda e: self.inverse_kinematics())
        self.inverse_kin_button.bind("<Enter>", lambda e: self.inverse_kin_button.config(image=self.button_image_hover))
        self.inverse_kin_button.bind("<Leave>", lambda e: self.inverse_kin_button.config(image=self.button_image))
        self.inverse_kin_button.pack(pady=30)

        self.path_following_button = tk.Label(self.center_frame, image=self.button_image, text="Path Following", compound="center", fg="white", font=('Helvetica', 24))
        self.path_following_button.bind("<Button-1>", lambda e: self.path_following())
        self.path_following_button.bind("<Enter>", lambda e: self.path_following_button.config(image=self.button_image_hover))
        self.path_following_button.bind("<Leave>", lambda e: self.path_following_button.config(image=self.button_image))
        self.path_following_button.pack(pady=30)

        # Add bottom frame for name and logo
        self.left_frame = tk.Frame(self.main_frame)
        self.left_frame.pack(side=tk.LEFT, fill=tk.X)

        # Display your name above the logo
        self.name_label = tk.Label(self.left_frame, text="Made by: Elena Villalba Aguilera", font=('Helvetica', 14)) # Replace with your name
        self.name_label.pack(side=tk.TOP, pady=(10, 0))

        # Display your name above the logo
        self.email_label = tk.Label(self.left_frame, text="    Contact: evillalba001@gmail.com", font=('Helvetica', 14)) # Replace with your name
        self.email_label.pack(side=tk.TOP, pady=(10, 0))
        
        # Add bottom frame for name and logo
        self.bottom_frame = tk.Frame(self.main_frame)
        self.bottom_frame.pack(side=tk.RIGHT, fill=tk.X)

        # Load and display the logo
        self.logo = Image.open("image/UPC_logo.png") 
        self.logo.thumbnail((200, 200), Image.LANCZOS)
        self.logo_image = ImageTk.PhotoImage(self.logo)
        self.logo_label = tk.Label(self.bottom_frame, image=self.logo_image)
        self.logo_label.pack(side=tk.BOTTOM, padx=10, pady=10)

        # Set up handling of window close event
        self.root.protocol("WM_DELETE_WINDOW", self.exit_handler)
        signal.signal(signal.SIGINT, self.signal_handler)

        self.root.mainloop() # Start the GUI event loop
                
    def create_rounded_rectangle_image(self, width, height, radius, color):
        image = Image.new("RGBA", (width, height))
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((0, 0, width, height), radius, fill=color)
        return ImageTk.PhotoImage(image)
     
    # Destroy the current window and start Forward Kinematics simulation
    def forward_kinematics(self):
        self.root.destroy()
        self.forward_kinematics_class.init_simulation(self.show_main_window)
        
    # Destroy current window and start Inverse Kinematics simulation
    def inverse_kinematics(self):
        self.root.destroy() 
        self.inverse_knimatics_class.init_simulation(self.show_main_window)
        
    # Destroy current window and start Path Following simulation
    def path_following(self):
        self.root.destroy() 
        self.path_following_class.init_simulation(self.show_main_window)

    # Function to show the main window after a simulation ends 
    def show_main_window(self):
        del self.root # Delete current window instance and initialize a new one
        self.init()
    
    # Function to handle Ctrl+C signal
    def signal_handler(self, sig, frame):
        print("Ctrl+C pressed. Exiting...")
        self.exit_handler()
    
    # Function to handle program exit
    def exit_handler(self):
        print("Exiting...")
        self.root.quit()
        sys.exit()
            
if __name__ == "__main__":
    gui = RobotSimGUI()