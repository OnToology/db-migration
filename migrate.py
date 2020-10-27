

def get_code_per_user(ouser):
    txt = ""
    user_txt = '''user = OUser.objects.create_user(email="%s", username="%s", password="%s", token="%s")\n''' % (
        ouser.email, ouser.username, ouser.password, ouser.token)
    txt += user_txt
    for repo in ouser.repos:
        repo_txt = '''repo = Repo(url="%s", state="Ready", previsual=False, previsual_page_available=False, notes="",
        progress=0.0, busy=False)\n''' % (repo.url)
        repo_txt += '''repo.save()\n'''
        txt += repo_txt
        pnames = PublishName.objects.filter(repo=repo, user=ouser)
        for p in pnames:
            publish_txt = '''p = PublishName(name="%s", user=user, repo=repo, ontology="%s")\n''' % (p.name, p.ontology)
            publish_txt += '''p.save()\n'''
            txt += publish_txt
    return txt


def generate_code():
    txt = ""
    users = OUser.objects.all()
    for ouser in users:
        txt += get_code_per_user(ouser)
    return txt


txt = generate_code()
f = open("local_migrate.py", "w")
f.write(txt)
f.close()

