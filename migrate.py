

def user_code(ouser):
    user_get = '''users = OUser.objects.filter(email="%s")\n''' % (ouser.email)
    user_if = '''if len(users) == 0:\n'''
    user_crt = '''\tuser = OUser.objects.create_user(email="%s", username="%s", password="%s", token="%s")\n''' % (
        ouser.email, ouser.username, ouser.password, ouser.token)
    user_else = '''else:\n'''
    user_else_get = '''\tuser = users[0]\n'''
    txt = user_get + user_if + user_crt + user_else + user_else_get
    return txt


def append_repo_code():
    if_repo = '''if repo not in user.repos.all():\n'''
    append_repo = '''\tuser.repos.add(repo)\n'''
    append_save = '''\tuser.save()\n'''
    txt = if_repo + append_repo + append_save
    return txt


def repo_code(repo):
    repo_get = '''repos = Repo.objects.filter(url="%s")\n''' % (repo.url)
    repo_if = '''if len(repos) == 0:\n'''
    repo_crt = '''\trepo = Repo(url="%s", state="Ready", notes="", progress=0.0)\n''' % (repo.url)
    repo_save = '''\trepo.save()\n'''
    repo_else   = '''else:\n'''
    repo_else_body = '''\trepo = repos[0]\n'''
    txt = repo_get + repo_if + repo_crt + repo_save + repo_else + repo_else_body
    return txt


def publish_code(pname):
    publish_txt = '''p = PublishName(name="%s", user=user, repo=repo, ontology="%s")\n''' % (pname.name, pname.ontology)
    publish_txt += '''p.save()\n'''
    return publish_txt


def get_code_per_user(ouser):
    user_txt = user_code(ouser)
    txt = user_txt
    for repo in ouser.repos:
        repo_txt = repo_code(repo)
        repo_txt += append_repo_code()
        # repo_txt = '''repo = Repo(url="%s", state="Ready", previsual=False, previsual_page_available=False, notes="",
        # progress=0.0, busy=False)\n''' % (repo.url)
        # repo_txt += '''repo.save()\n'''
        # txt += repo_txt
        pnames = PublishName.objects.filter(repo=repo, user=ouser)
        publish_txt = ""
        for p in pnames:
            # publish_txt = '''p = PublishName(name="%s", user=user, repo=repo, ontology="%s")\n''' % (p.name, p.ontology)
            # publish_txt += '''p.save()\n'''
            publish_txt += publish_code(pname)
        txt += repo_txt + publish_txt
    return txt


def generate_code():
    txt = ""
    users = OUser.objects.all()
    for ouser in users:
        txt += get_code_per_user(ouser)
        txt += "\n"
    return txt


def generate(fname="local_migrate.py"):
    txt = generate_code()
    f = open(fname, "w")
    f.write(txt)
    f.close()

