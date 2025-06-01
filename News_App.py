import requests
from tkinter import *
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageTk
from tkinter import messagebox, filedialog
import webbrowser  # To open URLs
from datetime import datetime #to update rgularly

# Initialize main window
root = Tk()
root.title('News App')
root.geometry('1000x700')
bg_color = "#404040"
text_area_bg = "#ffffff"
basic_font_color = "#ffffff"

def resize_image(event):
    new_width = event.width
    new_height = event.height
    resized_image = image.resize((new_width, new_height))
    photo = ImageTk.PhotoImage(resized_image)
    background_label.config(image=photo)
    background_label.image = photo  # Keep a reference to avoid garbage collection

# Background image
image_path = "news2.jpg"
image = Image.open(image_path)
photo = ImageTk.PhotoImage(image)

background_label = Label(root, image=photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
root.bind("<Configure>", resize_image)

# Create a frame for input section
input_frame = Frame(root, bg=bg_color, bd=10, relief=RIDGE)
input_frame.place(relx=0.5, rely=0.10, anchor=CENTER, width=600, height=100)

def new_file():
    newstxt.configure(state='normal')
    newstxt.delete('1.0', END)
    print("New file created!")  # Placeholder for functionality

def show_about():
    messagebox.showinfo("About", "This is a simple menu example using Tkinter.")
    
# Create the menu
menu = Menu(root)
root.config(menu=menu)

# File menu
filemenu = Menu(menu)
menu.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label='New', command=new_file)
filemenu.add_separator()
filemenu.add_command(label='Exit', command=root.quit)

# Help menu
helpmenu = Menu(menu)
menu.add_cascade(label='Help', menu=helpmenu)
helpmenu.add_command(label='About', command=show_about)


# Entry box for the topic
topic_label = Label(input_frame, text="Enter a topic:", font=("Helvetica", 16, "bold"), bg=bg_color, fg=basic_font_color)
topic_label.grid(row=0, column=0, padx=20, pady=10, sticky=W)

txt = Entry(input_frame, font=("Helvetica", 14), width=31)
txt.grid(row=0, column=1, padx=20, pady=20)

# Function to open URL in default browser
def open_url(url):
    webbrowser.open_new(url)

# ScrolledText for displaying news
output_frame = Frame(root, bg=bg_color, bd=15, relief=RIDGE)
output_frame.place(relx=0.5, rely=0.50, anchor=CENTER, width=1000, height=440)

newstxt = scrolledtext.ScrolledText(output_frame, width=80, height=20, font=("Helvetica", 14), bg=text_area_bg, fg="black", wrap=WORD)
newstxt.pack(expand=True, fill=BOTH)
newstxt.configure(state='disabled')


# Function to bind the clickable URL
def add_clickable_url(tag_name, url):
    newstxt.tag_bind(tag_name, "<Button-1>", lambda e: open_url(url))

# Function to fetch news
def newss():
    topic = txt.get()
    current_date = datetime.now().strftime("%Y-%M-%D")
    url = f"https://newsapi.org/v2/everything?q={topic}&from={current_date}&sortBy=publishedAt&apiKey=YOUR_API_KEY"
    
    try:
        r = requests.get(url)
        r.raise_for_status()
        news = r.json()

        newstxt.configure(state='normal')
        newstxt.delete('1.0', END)

        # Track unique articles using their URLs
        displayed_urls = set()

        if 'articles' in news and len(news['articles']) > 0:
            for i, article in enumerate(news['articles']):
                author = article.get("author", "Unknown")
                title = article.get("title", "No Title")
                description = article.get("description", "No Description")
                article_url = article.get("url", None)  # Use article_url here

                # Check if the article has already been displayed
                if article_url and article_url not in displayed_urls:
                    displayed_urls.add(article_url)  # Add URL to the set

                    # Insert news content
                    content = f"{len(displayed_urls)}. Title: {title}\nAuthor: {author}\nDescription: {description}\n\n"
                    newstxt.insert(END, content)

                    # Insert clickable URL
                    newstxt.insert(END, "Read more here\n", f"link_{len(displayed_urls) - 1}")
                    newstxt.insert(END, "\n________________________\n\n")

                    # Bind the tag with the correct article URL
                    add_clickable_url(f"link_{len(displayed_urls) - 1}", article_url)
                else:
                    continue  # Skip if the article is a duplicate
                
        else:
            newstxt.insert(END, "No news articles found for this topic.")

        newstxt.configure(state='disabled')
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to retrieve news: {e}")


# Fetch news function
def clicked():
    messagebox.showinfo('Message', 'Fetching latest news, please wait!')
    newss()



# Styled buttons for 'Enter' and 'Exit'
button_frame = Frame(root, bg=bg_color)
button_frame.place(relx=0.5, rely=0.91, anchor=CENTER)

btn = Button(button_frame, text='ENTER', font=("Helvetica", 15, "bold"), bg="#228B22", fg="white", width=10, height=2, command=clicked)
btn.grid(row=0, column=0, padx=20, pady=20)



button = Button(button_frame, text='EXIT', font=("Helvetica", 15, "bold"), bg="#B22222", fg="white", width=10, height=2, command=root.destroy)
button.grid(row=0, column=1, padx=20, pady=20)

root.mainloop()
