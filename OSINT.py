import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests
from bs4 import BeautifulSoup
import webbrowser

def search_google(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        for g in soup.find_all('div', class_='g'):
            title = g.find('h3').text if g.find('h3') else 'No title'
            link = g.find('a')['href'] if g.find('a') else 'No link'
            snippet = g.find('span', class_='aCOpRe').text if g.find('span', class_='aCOpRe') else 'No snippet'
            results.append({'title': title, 'link': link, 'snippet': snippet})
        return results
    else:
        return []

def search_social(search_query):
    api_key = 'YOUR_SOCIAL_SEARCHER_API_KEY'
    url = f"https://api.social-searcher.com/v2/search"
    params = {
        'q': search_query,
        'network': 'facebook,twitter,instagram,linkedin,youtube',
        'key': api_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {}

def perform_search():
    person_name = entry.get()
    if not person_name:
        messagebox.showwarning("Input Error", "Please enter a person's name")
        return

    google_results = search_google(person_name)
    social_results = search_social(person_name)

    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    
    result_text.insert(tk.END, "Google Search Results:\n\n")
    for result in google_results:
        result_text.insert(tk.END, f"Title: {result['title']}\n", 'bold')
        result_text.insert(tk.END, f"Link: {result['link']}\n", ('link', result['link']))
        result_text.insert(tk.END, f"Snippet: {result['snippet']}\n\n")
    
    result_text.insert(tk.END, "Social Media Search Results:\n\n")
    for post in social_results.get('posts', []):
        result_text.insert(tk.END, f"Date: {post['posted']}\n")
        result_text.insert(tk.END, f"Network: {post['network']}\n")
        result_text.insert(tk.END, f"User: {post['user']['name']}\n")
        result_text.insert(tk.END, f"Text: {post['text']}\n")
        result_text.insert(tk.END, f"Link: {post['url']}\n\n", ('link', post['url']))

    result_text.config(state=tk.DISABLED)

def open_link(event):
    tag_index = result_text.index(tk.CURRENT)
    tags = result_text.tag_names(tag_index)
    for tag in tags:
        if tag.startswith("http"):
            webbrowser.open(tag)
            return

app = tk.Tk()
app.title("OSINT Tool")

tk.Label(app, text="Enter the person's name:").pack(pady=5)
entry = tk.Entry(app, width=50)
entry.pack(pady=5)

tk.Button(app, text="Search", command=perform_search).pack(pady=10)

result_text = scrolledtext.ScrolledText(app, width=80, height=20, state=tk.DISABLED)
result_text.pack(pady=5)

result_text.tag_configure('bold', font=('Helvetica', 10, 'bold'))
result_text.tag_configure('link', foreground='blue', underline=True)
result_text.tag_bind('link', '<Button-1>', open_link)

app.mainloop()
