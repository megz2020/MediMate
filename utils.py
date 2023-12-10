def save_uploaded_file(uploaded_file, save_path):
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())


def convert_text_to_dict(text):
    try:
        text_str = ' '.join(text)
        dictionary = eval('{' + text_str + '}')
        return dictionary
    except Exception as e:
        print(f"Error converting text to dictionary: {e}")
        return None
    