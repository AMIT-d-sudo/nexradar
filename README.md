# Nexradar – AI-Powered Network Scanner

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Nexradar** एक स्मार्ट नेटवर्क स्कैनिंग टूल है जो **Nmap** का उपयोग करता है और **Artificial Intelligence (AI)** के जरिए स्कैन परिणामों का विश्लेषण करता है। यह सामान्य पोर्ट स्कैन से आगे बढ़कर, पैटर्न पहचान और विसंगतियों (anomalies) का पता लगाता है।

## ✨ विशेषताएँ (Features)

- Nmap के माध्यम से तीव्र और विस्तृत नेटवर्क स्कैन  
- **AI** – स्कैन आउटपुट से संभावित सुरक्षा कमजोरियों का अनुमान  
- स्वचालित रिपोर्ट जनरेशन (JSON / HTML)  
- कमांड-लाइन इंटरफेस, आसान उपयोग  

## 🧠 AI कैसे काम करता है? (How AI works)

Nmap के XML आउटपुट को पढ़ता है। मॉडल निम्नलिखित कार्य करता है:

- खुले पोर्ट के पैटर्न को पहचानना  
- असामान्य सर्विस वर्जन का पता लगाना  
- हर होस्ट के लिए **जोखिम स्कोर (0-100)** निकालना  

> **ध्यान दें:** आप चाहें तो अपने डेटा से पुनः प्रशिक्षित कर सकते हैं।

## 📋 आवश्यकताएँ (Requirements)

- **Nmap** (>=7.80) – [डाउनलोड](https://nmap.org/download.html)  
- **Python 3.8+**  
- Python पैकेज: `nmap`, `python-nmap` 'cryptography, `psutil`, `requests`'dnspython'  

## ⚙️ इंस्टॉलेशन (Installation)

```bash
# 1. रिपॉजिटरी क्लोन करें
git clone https://github.com/your-username/nexradar.git
cd nexradar

# 2. आवश्यक पैकेज इंस्टॉल करें
pip install -r requirements.txt
