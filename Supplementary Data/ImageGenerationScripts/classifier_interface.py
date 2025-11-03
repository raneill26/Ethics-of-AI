from flask import Flask, request, redirect, send_from_directory
import os
import pandas as pd
from flask import render_template_string

app = Flask(__name__)

DATA_DIR = "/Users/maxdale/Pictures/COMP 560/Output"
CSV_FILE = os.path.join(DATA_DIR, "monk_skin_tone_classification.csv")
THUMBNAIL_DIR = os.path.abspath(DATA_DIR)
current_index = 0

@app.route('/<path:filename>')
def serve_image(filename):
    global current_index
    return send_from_directory(THUMBNAIL_DIR, filename)

@app.route('/')
def index():
    global current_index
    try:
        df = pd.read_csv(CSV_FILE)
    except pd.errors.EmptyDataError:
        return "<h2>CSV is empty.</h2>"

    df['monk_label'] = df['monk_label'].astype(str)
    df['gender'] = df['gender'].astype(str)
    if current_index >= len(df):
        incomplete = df[(df['monk_label'] == '') | (df['gender'] == '')]
        current_index = int(incomplete.index[0]) if not incomplete.empty else 0
    idx = current_index
    if idx >= len(df):
        idx = len(df) - 1 if len(df) > 0 else 0
        current_index = idx

    row = df.iloc[idx]
    face_path = os.path.join(row["model"], row["job"], row["face_image"])
    monk_label = row.get("monk_label", "")
    gender = row.get("gender", "")

    progress = int((idx / len(df)) * 100)

    sorted_df = df[df['monk_label'].notna() | df['gender'].notna()].copy()
    sorted_df['_updated'] = sorted_df.index
    sorted_df = sorted_df.sort_values('_updated', ascending=False).head(20)

    unsorted_df = df[df['monk_label'].isna() & df['gender'].isna()]
    display_df = pd.concat([sorted_df, unsorted_df], ignore_index=True).drop(columns=['_updated'], errors='ignore')

    df_html = display_df.style.set_table_attributes('style="width:100%;font-size:12px;"').hide(axis='index').to_html()

    return render_template_string("""
    <html><head><title>Image Classifier</title>
    <style>
    body { font-family: sans-serif; margin: 20px; }
    img { width: 100%; max-width: 600px; height: auto; border: 4px solid #ddd; }
    .container { display: flex; }
    .left { width: 40%; padding-right: 20px; }
    .right { width: 60%; overflow-x: auto; }
    #monk_label { display: flex; flex-wrap: wrap; gap: 16px; justify-content: center; padding: 10px 0; }
    </style>
    </head><body>
    <h2>Progress: {{ idx + 1 }} / {{ total }} ({{ progress }}%)</h2>
    <form method="post" action="/goto" style="margin-bottom: 20px;">
        <label for="target_row">Go to row:</label>
        <input type="number" name="target_row" id="target_row" min="0" max="{{ total - 1 }}" value="{{ idx }}" style="width: 80px;">
        <button type="submit">Go</button>
    </form>
    <div class="container">
        <div class="left">
            <img src="/{{ face_path }}" alt="Face" style="max-width:100%;height:auto;max-height:400px;border:4px solid #ddd;">
            <form method='post' action='/submit'>
                <label>Monk Label:</label><br>
                <div id="monk_label">
                    {% set monk_colors = ['#FDF6EC', '#F3E2D2', '#EED1B4', '#D6A77A', '#BC8753', '#A36D3E', '#895431', '#6C3F2A', '#3E2D26', '#2D211C'] %}
                    {% for i in range(1, 11) %}
                    <label style="display: flex; flex-direction: column; align-items: center; cursor: pointer; width: 60px; margin-bottom: 10px; transition: transform 0.2s; border: 2px solid {% if i|string == monk_label|string %}#007bff{% else %}transparent{% endif %}; border-radius: 8px; padding: 4px;">
                        <input type="radio" name="monk_label" value="{{ i }}" {% if i|string == monk_label|string %}checked{% endif %} style="display: none;">
                        <div style="width: 48px; height: 48px; border-radius: 50%; background-color: {{ monk_colors[i-1] }}; border: 2px solid #666; box-shadow: 0 2px 6px rgba(0,0,0,0.2);"></div>
                        <span style="margin-top: 5px; font-size: 12px; font-weight: bold;">{{ i }}</span>
                    </label>
                    {% endfor %}
                </div>
                <br>
                <label>Gender:</label><br>
                <div id="gender_selector" style="display: flex; gap: 10px; margin: 10px 0;">
                    {% for g in ['Male', 'Female', 'Other'] %}
                    <label style="padding: 6px 12px; border: 2px solid {% if g == gender %}#007bff{% else %}#ccc{% endif %}; border-radius: 6px; cursor: pointer; background-color: {% if g == gender %}#e7f0ff{% else %}white{% endif %}; font-weight: bold;">
                        <input type="radio" name="gender" value="{{ g }}" {% if g == gender %}checked{% endif %} style="display: none;">
                        {{ g }}
                    </label>
                    {% endfor %}
                </div>
                <br>
                <button type="submit">Submit</button>
            </form>
            <form method='post' action='/back'><button type='submit'>Back</button></form>
            <form method='post' action='/delete'><button type='submit'>Delete</button></form>
        </div>
        <div class="right">{{ df_html|safe }}</div>
    </div>
    {% raw %}
    <script>
    document.addEventListener('keydown', function(e) {
        const activeTag = document.activeElement.tagName.toLowerCase();
        if (activeTag === 'input' || activeTag === 'select' || activeTag === 'textarea') return;

        let value = null;
        if (e.key >= '1' && e.key <= '9') value = e.key;
        else if (e.key === '0') value = '10';

        if (value) {
            const input = document.querySelector(`input[name="monk_label"][value="${value}"]`);
            if (input) {
                input.checked = true;
                input.dispatchEvent(new Event('change', { bubbles: true }));
                input.closest('label').scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }

        const genderMap = {
            'm': 'Male',
            'f': 'Female',
            'o': 'Other'
        };

        if (genderMap[e.key.toLowerCase()]) {
            const gInput = document.querySelector(`input[name="gender"][value="${genderMap[e.key.toLowerCase()]}"]`);
            if (gInput) {
                gInput.checked = true;
                gInput.dispatchEvent(new Event('change', { bubbles: true }));
                gInput.closest('label').scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }

        if (e.key === 'Enter') {
            e.preventDefault();
            document.forms[0].submit();
        }
    });
    </script>
    {% endraw %}
    </body></html>
    """, idx=idx, total=len(df), progress=progress, face_path=face_path, monk_label=monk_label, gender=gender, df_html=df_html)

@app.route('/submit', methods=['POST'])
def submit():
    global current_index
    df = pd.read_csv(CSV_FILE)
    idx = current_index
    monk = request.form.get('monk_label', '').strip()
    gender = request.form.get('gender', '').strip()
    print(f" SUBMIT row {idx} → monk_label={monk}, gender={gender}")

    if idx < len(df):
        if monk:
            df.at[idx, 'monk_label'] = monk
        if gender:
            df.at[idx, 'gender'] = gender
        df.to_csv(CSV_FILE, index=False)

    df = pd.read_csv(CSV_FILE)
    df['monk_label'] = df['monk_label'].astype(str).str.strip()
    df['gender'] = df['gender'].astype(str).str.strip()

    next_idx = idx + 1 if idx + 1 < len(df) else idx
    current_index = int(next_idx)

    return redirect('/')

@app.route('/back', methods=['POST'])
def go_back():
    global current_index
    idx = current_index
    current_index = max(0, idx - 1)
    return redirect('/')

@app.route('/delete', methods=['POST'])
def delete_row():
    global current_index
    df = pd.read_csv(CSV_FILE)
    idx = current_index
    if idx < len(df):
        df = df.drop(index=idx).reset_index(drop=True)
        df.to_csv(CSV_FILE, index=False)
        current_index = max(0, idx - 1)
    return redirect('/')

@app.route('/skip', methods=['POST'])
def skip_row():
    global current_index
    df = pd.read_csv(CSV_FILE)
    df['monk_label'] = df['monk_label'].astype(str)
    df['gender'] = df['gender'].astype(str)
    incomplete = df[(df['monk_label'] == '') | (df['gender'] == '')]
    idx = incomplete.index[0] if not incomplete.empty else len(df) - 1
    current_index = int(idx)
    return redirect('/')

@app.route('/goto', methods=['POST'])
def go_to_row():
    global current_index
    try:
        target = int(request.form.get('target_row', 0))
        df = pd.read_csv(CSV_FILE)
        if 0 <= target < len(df):
            current_index = target
    except Exception as e:
        print("Failed to go to row:", e)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)