
<div align="center" style="margin-bottom:30px;">
  <img width="150" alt="comments analytics logo" src="https://github.com/user-attachments/assets/4a6980a1-582b-43a2-b197-e6c418dc53c9" />
</div>
<br><br> <!-- add more <br> if you need more space -->



# Comments Analytics

Analyze and understand comments from YouTube, social media, and other platforms with **Comments Analytics**.  
This project provides tools for **sentiment analysis, keyword extraction, named entity recognition (NER), and comment categorization**, helping creators, businesses, and researchers gain insights from user feedback at scale.

---

## 🚀 Features
- 🔍 **Sentiment Analysis** – Detect positive, negative, and neutral comments.  
- 🏷 **Keyword Extraction** – Automatically highlight trending topics and repeated phrases.  
- 🧾 **Named Entity Recognition (NER)** – Identify people, places, brands, and other named entities mentioned in comments.  
- 📂 **Categorization** – Group comments into categories (e.g., feedback, questions, spam).  
- 📊 **Analytics Dashboard** – Visualize engagement and sentiment distribution.  
- ⚡ **Batch Processing** – Analyze thousands of comments at once.  


---

## 📦 Installation
Clone this repository and install dependencies:

```bash
git clone https://github.com/your-username/comments-analytics.git
cd comments-analytics
pip install -r requirements.txt
```

---

## 🛠 Usage
### Example: Sentiment Analysis
```python
from commentsanalytics import analyze_sentiment

comment = "I love this video, it’s really helpful!"
result = analyze_sentiment(comment)
print(result)  # Output: {"label": "positive", "score": 0.92}
```


<div align="center" style="margin-bottom:30px;">
  <img width="1084" height="387" alt="sentiment" src="https://github.com/user-attachments/assets/a09a05d0-d261-447e-b20f-f55b40091ded" />
</div>
<br><br> <!-- add more <br> if you need more space -->

### Example: Keyword Extraction
```python
from commentsanalytics import extract_keywords

comments = [
    "This tutorial is awesome!",
    "Great video, I learned so much about Python.",
    "Could you make more videos on web scraping?"
]

keywords = extract_keywords(comments)
print(keywords)
# Output: ["tutorial", "Python", "web scraping", "video"]
```


<div align="center" style="margin-bottom:30px;">
  <img width="1079" height="517" alt="wordcloud" src="https://github.com/user-attachments/assets/a6986aa5-2154-431f-a4d8-d04b3f53c65b" />
</div>
<br><br> <!-- add more <br> if you need more space -->
---

## 🌐 Live Demo
👉 Check out the live version here: [commentsanalytics.com](https://commentsanalytics.com)

---

## 📊 Use Cases
- 🎥 **Content Creators** – Understand audience reactions to videos.  
- 🏢 **Businesses** – Track customer feedback across social platforms.  
- 📚 **Researchers** – Study online discourse at scale.  
- 🤖 **Developers** – Build apps that integrate advanced comment analytics.  

---

## 🛤 Roadmap
- [ ] Add support for more platforms (Instagram, TikTok).  
- [ ] Advanced visualization dashboard.  
- [ ] Export results in CSV/Excel.  
- [ ] Real-time streaming analysis.  

---

## 🤝 Contributing
Contributions are welcome! Please open an issue or submit a pull request to discuss improvements.  

---

## 📜 License
This project is licensed under the [MIT License](LICENSE).  

---

## 🙌 Acknowledgements
- Built with ❤️ in Python & Django.  
- NLP powered by spaCy / HuggingFace Transformers.  


---

## 📬 Contact
**Developer:** Taha Hamedani  
**Email:** taha.hamedani8@gmail.com  
