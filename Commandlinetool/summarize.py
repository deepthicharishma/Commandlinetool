import click
import requests
import chardet
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

MODEL = "llama2"

def summarize_text(text):
    url = "http://localhost:11434/api/generate"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "prompt": f"Please summarize the following text:\n\n{text}",
        "stream": False
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        summary = response.json().get("response", "No summary provided")
        return summary.strip()
    except requests.exceptions.RequestException as e:
        return f"Error: Request failed - {str(e)}"
    except Exception as e:
        return f"Error: An unexpected error occurred - {str(e)}"

@click.command()
@click.option('-t', '--textfile', type=click.Path(exists=True), help='Path to the text file to summarize')
@click.argument('text', required=False)
def main(textfile, text):
    if textfile:
        try:
            with open(textfile, 'r', encoding='utf-8') as file:
                text = file.read()
        except UnicodeDecodeError:
            with open(textfile, 'rb') as file:
                raw_data = file.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            try:
                with open(textfile, 'r', encoding=encoding) as file:
                    text = file.read()
            except UnicodeDecodeError as e:
                print(f"Error: Unable to read file - {str(e)}")
                return
    elif not text:
        print("Error: Please provide either a text file or direct text input.")
        return

    summary = summarize_text(text)
    print(summary)

if __name__ == "__main__":
    main()
