from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        url = f"https://api.github.com/users/{username}"
        response = requests.get(url)
        if response.status_code != 200:
            return render_template('profile.html', error="GitHub user not found.")
        
        user_data = response.json()
        repos_data = requests.get(user_data['repos_url']).json()
        top_repos = sorted(repos_data, key=lambda r: r['stargazers_count'], reverse=True)[:3]

        return render_template('profile.html', user=user_data, top_repos=top_repos)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)