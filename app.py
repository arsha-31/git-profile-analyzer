from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        user_url = f"https://api.github.com/users/{username}"
        user_resp = requests.get(user_url)

        if user_resp.status_code != 200:
            return render_template('profile.html', error="GitHub user not found or API limit reached.")

        user_data = user_resp.json()

        repos_resp = requests.get(user_data['repos_url'])
        repos_data = repos_resp.json()

        total_stars = 0
        for repo in repos_data:
            total_stars += repo['stargazers_count']
            # Fetch top 3 languages for each repo
            lang_resp = requests.get(repo['languages_url'])
            if lang_resp.status_code == 200:
                langs = list(lang_resp.json().keys())[:3]
                repo['languages'] = ', '.join(langs)
            else:
                repo['languages'] = "N/A"

        top_repos = sorted(repos_data, key=lambda r: r['stargazers_count'], reverse=True)[:3]

        return render_template(
            'profile.html',
            user=user_data,
            top_repos=top_repos,
            total_stars=total_stars
        )

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
