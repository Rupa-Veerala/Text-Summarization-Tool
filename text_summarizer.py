import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox, font
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import heapq
import string
import nltk

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')

class TextSummarizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Summarization Tool")
        self.root.geometry("1000x800")
        
        # Set up style
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10, 'bold'))
        
        # Configure root window
        self.root.configure(bg='#f0f0f0')
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create title frame
        title_frame = ttk.Frame(self.main_frame)
        title_frame.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        title_label = ttk.Label(title_frame, text="Text Summarization Tool", 
                              font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0)
        
        # Create input text area
        input_frame = ttk.LabelFrame(self.main_frame, text="Input Text", padding="5")
        input_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        self.input_text = scrolledtext.ScrolledText(input_frame, 
                                                    width=60, 
                                                    height=10,
                                                    font=('Arial', 10))
        self.input_text.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        # Create buttons frame
        buttons_frame = ttk.Frame(self.main_frame)
        buttons_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.upload_button = ttk.Button(buttons_frame, 
                                       text="Upload Text File", 
                                       command=self.upload_file,
                                       style='TButton')
        self.upload_button.grid(row=0, column=0, padx=5)
        
        self.summarize_button = ttk.Button(buttons_frame, 
                                          text="Generate Summary", 
                                          command=self.summarize_text,
                                          style='TButton')
        self.summarize_button.grid(row=0, column=1, padx=5)
        
        # Create summary text area
        summary_frame = ttk.LabelFrame(self.main_frame, text="Summary", padding="5")
        summary_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        self.summary_text = scrolledtext.ScrolledText(summary_frame, 
                                                      width=60, 
                                                      height=10,
                                                      font=('Arial', 10))
        self.summary_text.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        # Create options frame
        options_frame = ttk.LabelFrame(self.main_frame, text="Options", padding="10")
        options_frame.grid(row=4, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        # Summary length slider
        self.summary_length = tk.IntVar(value=5)
        
        length_frame = ttk.Frame(options_frame)
        length_frame.grid(row=0, column=0, pady=5)
        
        ttk.Label(length_frame, text="Summary Length:").grid(row=0, column=0, padx=5)
        
        length_slider = ttk.Scale(length_frame, 
                                 from_=1, 
                                 to=20, 
                                 variable=self.summary_length,
                                 orient=tk.HORIZONTAL)
        length_slider.grid(row=0, column=1, padx=5)
        
        ttk.Label(length_frame, textvariable=self.summary_length).grid(row=0, column=2, padx=5)
        
        # Add tooltips
        self.add_tooltip(self.upload_button, "Upload a text file to summarize")
        self.add_tooltip(self.summarize_button, "Generate summary from input text")
        
    def add_tooltip(self, widget, text):
        """Add a tooltip to a widget"""
        def enter(event):
            x = y = 0
            x, y, cx, cy = widget.bbox("insert")
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 20
            
            # Create tooltip
            self.tooltip = tk.Toplevel(widget)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_geometry(f"+{x}+{y}")
            
            label = ttk.Label(self.tooltip, text=text, background="white", relief='solid', borderwidth=1)
            label.pack(ipadx=1)
            
        def leave(event):
            if hasattr(self, 'tooltip'):
                self.tooltip.destroy()
                del self.tooltip
        
        widget.bind('<Enter>', enter)
        widget.bind('<Leave>', leave)
        
    def upload_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.input_text.delete(1.0, tk.END)
                    self.input_text.insert(tk.END, content)
                    messagebox.showinfo("Success", "File uploaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read file: {str(e)}")
    
    def summarize_text(self):
        try:
            # Get input text
            text = self.input_text.get(1.0, tk.END).strip()
            if not text:
                messagebox.showwarning("Input Error", "Please enter or upload some text first!")
                return
            
            # Calculate input statistics
            input_word_count = len(nltk.word_tokenize(text))
            input_sentence_count = len(sent_tokenize(text))
            input_char_count = len(text)
            
            print("\nInput Text Statistics:")
            print("-" * 50)
            print(f"Total Characters: {input_char_count}")
            print(f"Total Words: {input_word_count}")
            print(f"Total Sentences: {input_sentence_count}")
            print("-" * 50)
            
            # Clean and preprocess text
            text = text.lower()
            text = text.translate(str.maketrans('', '', string.punctuation))
            
            # Tokenize sentences
            sentences = sent_tokenize(text)
            
            if not sentences:
                messagebox.showerror("Error", "No sentences found in the text!")
                return
                
            # Create word frequency dictionary
            word_frequencies = {}
            stop_words = set(stopwords.words('english'))
            
            # Calculate word frequencies
            words = nltk.word_tokenize(text)
            
            for word in words:
                if word not in stop_words:
                    if word not in word_frequencies.keys():
                        word_frequencies[word] = 1
                    else:
                        word_frequencies[word] += 1
            
            if not word_frequencies:
                messagebox.showerror("Error", "No valid words found after processing!")
                return
                
            # Normalize word frequencies
            max_freq = max(word_frequencies.values())
            for word in word_frequencies.keys():
                word_frequencies[word] = (word_frequencies[word] / max_freq)
            
            # Calculate sentence scores
            sentence_scores = {}
            
            for i, sentence in enumerate(sentences):
                sentence_length = len(nltk.word_tokenize(sentence))
                
                # Skip very short sentences
                if sentence_length < 30:
                    continue
                    
                # Calculate position score
                position_score = 0.5 if i == 0 else 0.3 if i == len(sentences) - 1 else 0.2
                
                # Calculate word importance score
                word_importance = 0
                for word in nltk.word_tokenize(sentence.lower()):
                    if word in word_frequencies.keys():
                        word_importance += word_frequencies[word]
                
                # Calculate final score
                if sentence_length > 0:
                    score = (word_importance / sentence_length) * 0.7 + position_score * 0.3
                    sentence_scores[sentence] = score
            
            if not sentence_scores:
                messagebox.showerror("Error", "No valid sentences found for summarization!")
                return
                
            # Get top N sentences
            summary_length = self.summary_length.get()
            if summary_length > len(sentence_scores):
                summary_length = len(sentence_scores)
                
            summary_sentences = heapq.nlargest(summary_length, sentence_scores, key=sentence_scores.get)
            
            # Sort sentences to maintain logical order
            summary_sentences = sorted(summary_sentences, key=lambda x: text.index(x))
            
            # Create summary
            summary = ' '.join(summary_sentences)
            
            # Calculate summary statistics
            summary_word_count = len(nltk.word_tokenize(summary))
            summary_sentence_count = len(summary_sentences)
            summary_char_count = len(summary)
            
            print("\nSummary Statistics:")
            print("-" * 50)
            print(f"Total Characters: {summary_char_count}")
            print(f"Total Words: {summary_word_count}")
            print(f"Total Sentences: {summary_sentence_count}")
            print(f"Compression Ratio: {input_word_count/summary_word_count:.2f}x")
            print("-" * 50)
            
            # Clear and insert summary
            self.summary_text.delete(1.0, tk.END)
            self.summary_text.insert(tk.END, summary)
            
            # Add success message
            messagebox.showinfo("Success", f"Summary generated successfully!\nLength: {summary_sentence_count} sentences")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            print(f"Error in summarization: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextSummarizer(root)
    root.mainloop()
