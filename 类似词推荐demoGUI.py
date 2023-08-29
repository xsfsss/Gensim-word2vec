import tkinter as tk
from tkinter import scrolledtext
import sys
from gensim.models import Word2Vec

en_wiki_word2vec_model = Word2Vec.load('wiki.zh.text.model')
testwords = []
def close_window():
    root.destroy()
    sys.exit()

def process_input():
    input_text = input_box.get("1.0", "end-1c")
    output_text.insert("end", f"Input: {input_text}\n")
    input_box.delete("1.0", "end")
    similar_process(input_text)

def similar_process(input_text):
    try:
        res = en_wiki_word2vec_model.wv.most_similar(input_text)
        top_words = res[:2]
        display_similarity_results(top_words)
    except KeyError:
        #print("触发Key error")
        display_Error()

def display_similarity_results(results):
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    for word, score in results:
        output_text.insert(tk.END, f" {word}  ")
    output_text.config(state=tk.DISABLED)

def display_Error():
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    error = ["词典中没有收录该词汇，无法查明"]
    output_text.insert(tk.END, f"Error: {error}  ")
    output_text.config(state=tk.DISABLED)


root = tk.Tk()
root.title("同类词推荐框")

# Input box
input_box = scrolledtext.ScrolledText(root, height=3, wrap=tk.WORD)
input_box.pack(padx=10, pady=10)

# Output box
output_text = scrolledtext.ScrolledText(root, height=3, wrap=tk.WORD, state=tk.DISABLED)
output_text.pack(padx=10, pady=5)

# Process button
process_button = tk.Button(root, text="Process Input", command=process_input)
process_button.pack()

# Close button
close_button = tk.Button(root, text="Close", command=close_window)
close_button.pack()

root.protocol("WM_DELETE_WINDOW", close_window)  # Handle window close event
root.mainloop()
