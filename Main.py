import requests
import csv
def user_details(username):
    url = f"https://api.github.com/users/{username}"
    data = requests.get(url, headers=auth_token).json()
    company=data['company'].strip().upper() if data['company'] else None
    if company and company.startswith('@'):
        company = company[1:]

    user_detail={
        'login':data['login'],
        'name':data['name'],
        'company':company,
        'location':data['location'],
        'email':data['email'],
        'hireable':data['hireable'],
        'bio':data['bio'],
        'public_repos':data['public_repos'],
        'followers':data['followers'],
        'following':data['following'],
        'created_at':data['created_at'],
    }
    return user_detail

token=input("Please enter the token number")
auth_token ={"Authorization": f"token {token}"}
users = []
query = "location:Beijing +followers:>500"
page = 1
per_page = 100
total_no_of_users = 0
while True:
   url = f"https://api.github.com/search/users?q={query}&per_page={per_page}&page={page}"
   response = requests.get(url, headers=auth_token)
   print(f"Loading & Fetching page {page}...")

   if response.status_code != 200:
      print("Error!Something wrong with Fetching:", response.json())
      break

   data = response.json()
   users.extend(data['items'])
   total_no_of_users += len(data['items'])
   if  per_page > len(data['items']) :
        break

   page += 1

print(page)
print(total_no_of_users)

user_information = []
for user in users:
   user_info = user_details(user['login'])
   user_information.append(user_info)


with open('users.csv', mode='w', newline='') as file:
     writer = csv.DictWriter(file, fieldnames=['login', 'name', 'company', 'location', 'email', 'hireable', 'bio', 'public_repos', 'followers', 'following', 'created_at'])
     writer.writeheader()
     writer.writerows(user_information)

def user_repos(username):
    repo_url = f"https://api.github.com/users/{username}/repos?per_page=500"
    response = requests.get(repo_url, headers=auth_token)
    repos_data = response.json()


    user_repos = []
    for repo in repos_data:
        user_repos.append({
            'login': username,
            'full_name': repo['full_name'],
            'created_at': repo['created_at'],
            'stargazers_count': repo['stargazers_count'],
            'watchers_count': repo['watchers_count'],
            'language': repo['language'],
            'has_projects': repo['has_projects'],
            'has_wiki': repo['has_wiki'],
            'license_name': repo['license']['key'] if repo['license'] else None,
        })

    return user_repos

all_repos = []
for user in users:
  repos =user_repos(user['login'])
  all_repos.extend(repos)

with open('repositories.csv', mode='w', newline='') as file:
     writer = csv.DictWriter(file, fieldnames=['login', 'full_name', 'created_at', 'stargazers_count', 'watchers_count', 'language', 'has_projects', 'has_wiki', 'license_name'])
     writer.writeheader()
     writer.writerows(all_repos)


print("Done")
