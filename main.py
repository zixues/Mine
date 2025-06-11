# import streamlit as st
# from urllib.parse import urlparse
# from scrape import (
#     scrape_website,
#     extract_body_content,
#     clean_body_content,
# )

# # Save content and URL into a domain-specific text file
# def save_dom_to_file(domain, cleaned_content, url):
#     filename = f"{domain}_dom_dump.txt"
#     with open(filename, "a", encoding="utf-8") as file:
#         file.write("\n" + "="*80 + "\n")
#         file.write(f"New entry from URL: {url}\n")
#         file.write("="*80 + "\n")
#         file.write(cleaned_content)
#         file.write("\n\n")

# # Streamlit UI
# st.title("AI Web Scraper (Save Only)")

# # Take 3 input URLs
# urls = [
#     st.text_input("Enter Website URL 1"),
#     st.text_input("Enter Website URL 2"),
#     st.text_input("Enter Website URL 3"),
# ]

# if st.button("Scrape and Save"):
#     for url in urls:
#         if url:
#             st.markdown(f"### Processing: {url}")
#             st.write("Scraping the website...")

#             try:
#                 # Scrape and clean
#                 dom_content = scrape_website(url)
#                 body_content = extract_body_content(dom_content)
#                 cleaned_content = clean_body_content(body_content)

#                 # Determine domain
#                 if "noon" in url:
#                     domain = "noon"
#                 elif "centrepoint" in url:
#                     domain = "centrepoint"
#                 elif "namshi" in url:
#                     domain = "namshi"
#                 else:
#                     domain = urlparse(url).netloc.split('.')[0]

#                 # Save to file
#                 save_dom_to_file(domain, cleaned_content, url)

#                 # Show success message and DOM
#                 st.success(f"Saved content for {url}")
#                 with st.expander(f"View Cleaned Content - {domain}"):
#                     st.text_area("Cleaned Content", cleaned_content, height=300)

#             except Exception as e:
#                 st.error(f"Failed to process {url}: {str(e)}")
from flask import Flask, request, jsonify
from scrape import scrape_website, extract_body_content, clean_body_content

app = Flask(__name__)

@app.route("/scrape", methods=["POST"])
def scrape():
    data = request.get_json(force=True)  # ensures JSON is parsed
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        dom_content = scrape_website(url)
        body_content = extract_body_content(dom_content)
        cleaned_content = clean_body_content(body_content)

        return jsonify({
            "url": url,
            "cleaned_dom": cleaned_content
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
