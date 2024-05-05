import argparse
from dotenv import load_dotenv
import pkg_resources
from os.path import abspath, isdir, join, pardir
from os import mkdir, walk
from os import getenv, environ
from pathlib import Path
import pathlib
from shutil import copyfile
from shutil import copytree, rmtree
import sys
import subprocess
import argparse
import yaml
# pip installs

from dotenv import load_dotenv

from Notion2Pelican.Notion2Pelican import readDatabase, page_tree_ids
from Notion2Pelican.Notion2Pelican import get_notion_headers, pageid_2_md

# locals
from wrapper_podcast import make_podcast


# generic pelican wrapper
www_folder_dev = abspath(join(__file__, pardir, "public_local"))
www_folder_staging = abspath(join(__file__, pardir, "public_nas"))
www_folder = abspath(join(__file__, pardir, "www_folder"))
pelican_dp = abspath(join(__file__, pardir, "static", "src"))
pelican_local_fp = abspath(join(pelican_dp, "pelicanconf.py"))
dp_notion = abspath(join(__file__, pardir, "notion"))
# tmp folder is where local files and Notion files are merged
dp_tmp = abspath(join(__file__, pardir, "tmp"))

pathlib.Path(dp_notion).mkdir(parents=True, exist_ok=True)
pathlib.Path(dp_tmp).mkdir(parents=True, exist_ok=True)
pathlib.Path(join(dp_tmp, "notion")).mkdir(parents=True, exist_ok=True)
pathlib.Path(www_folder).mkdir(parents=True, exist_ok=True)
pathlib.Path(www_folder_dev).mkdir(parents=True, exist_ok=True)

# add here local folders to be imported for any specific reason
# gist folder, pelican folder
# sys.path.insert(1, pelican_dp)
# prod gh-pages
podcast_rss_fn = "feed_new2.xml"
podcast_dir = join(www_folder_dev, "player", "web")


def check_venv(test_requirements=True):
    if test_requirements:
        installed_packages = pkg_resources.working_set
        installed_versionned_packages_list = sorted(["%s==%s" % (i.key, i.version)
        for i in installed_packages])
        installed_packages_list = sorted([i.key for i in installed_packages])
        # print(installed_packages_list)   
        # print(installed_versionned_packages_list)

    run_pelican = True
    for needed in ["pelican","jinja2","markdown","pelican-sitemap",
                   "pelican-more-categories"]:
        if needed not in installed_packages_list:
            print(f"missing {needed}")
            run_pelican=False

    if run_pelican:
        print("all needed packages are installed... now building")
    else:
        print("stopping here")
    
    return run_pelican


def pre_pelican(dp_content, theme, dp_www,
                build_flow,
                rebuild_tmp=False,
                rebuild_notion=False,
                dp_not=dp_notion):
    """ pelican wrapper, to be included here :
    1. check python dependancies
    2. generate index page for all draft pages
    2. TBD
    """
    check_venv()
    Path(dp_www).mkdir(parents=True, exist_ok=True)
    # list_drafts(dp_content,theme,dp_www)

    # if rebuild_notion
    # 1. delete notion folder in tmp
    # 2. download notion
    if rebuild_notion:
        print("updating notion in folder", dp_notion)
        pull_notion(dp_not=dp_notion, build_flow=build_flow)
        rmtree(join(dp_tmp, "notion"))
    else:
        print("NOTION **NOT** updated")

    # 3. copy the content folder into the tmp folder
    if rebuild_tmp:
        if pathlib.Path(dp_tmp).exists():
            rmtree(dp_tmp)
        dp_src = abspath(join(__file__, pardir, "content"))
        print("updating content in tmp folder", dp_src, dp_tmp)
        copytree(dp_src, dp_tmp)
        copytree(dp_notion, join(dp_tmp, "notion"))

    return dp_tmp


def pelican_wrapper(dp_content, theme, dp_www,
                    test_requirements=False,
                    pelican_e=None):
    """ add here code around pelican:
    a. check for required packages
    b. run specific actions (like own pelican extensions not available in 
        pelican repository...)

    old notes:
        fp_pelicanconf = abspath(join(__file__, pardir, "static","src","pelicanconf.py"))
        result = subprocess.run(["pelican", dp_content,
                                 "-t", "static/theme",
                                 "-o", dp_www,
                                 "-s", fp_pelicanconf], capture_output=True, text=True)


    """
    run_pelican = True
    fp_pelicanconf = abspath(join(__file__, pardir, "static","src","pelicanconf.py"))
    print(106, dp_content)

    if test_requirements:

        installed_packages = pkg_resources.working_set
        installed_versionned_packages_list = sorted(["%s==%s" % (i.key, i.version)
           for i in installed_packages])
        installed_packages_list = sorted([i.key for i in installed_packages])
        # print(installed_packages_list)   
        # print(installed_versionned_packages_list)

        
        for needed in ["pelican","jinja2","markdown","pelican-sitemap"]:
            if needed not in installed_packages_list:
                print(f"missing {needed}")
                run_pelican=False

    if run_pelican:
        pel_ags = ["pelican",dp_content,
                   "-t","static/theme","-o",www_folder,
                   "-s", fp_pelicanconf]
        if pelican_e:
            pel_ags.append("-e")
            for pel_e in pelican_e.split(" "):
                pel_ags.append(pel_e)
        result = subprocess.run(pel_ags, capture_output=True, text=True)
    return result


def post_pelican(dp_content, theme, dp_www, pelican_results, delete_tmp=False):
    """ pelican wrapper, to be included here :
    1. hidden page which has logs of last generated static site
    2. TBD
    """
    print("post pelican **************")
    print(pelican_results.stdout)
    print(pelican_results.stderr)
    if delete_tmp:
        if pathlib.Path(dp_tmp).exists():
            rmtree(dp_tmp)


def pull_notion(dp_not, build_flow):
    """ pulls the notion pages into the local file system. Not checks
    files will be overwritten.

    Parameters
    ----------
    dp_not: str
        the path where notion files shall be written.
    build_flow: str
        switch between loadenv and os.environ
    """
    load_dotenv()
    if build_flow=="gh":
        MY_NOTION_SECRET = environ["NOTIONKEY"]
        FT_dbid = environ["FT_dbid"]
    else:
        MY_NOTION_SECRET = getenv("NOTIONKEY")
        FT_dbid = getenv("FT_dbid")
    headers = get_notion_headers(MY_NOTION_SECRET)
    # notion_db_id = MY_NOTION_DB_ID
    res = readDatabase(databaseId=FT_dbid, notion_header=headers)
    site_tree = page_tree_ids(res, headers)
    draft_folder = ""
    content_folder = dp_not
    page_folder = ""
    for page in site_tree:
        # print(103, page["title"])
        if page["title"]=="Published":
            dpo = content_folder
            status= "published"
        elif page["title"]=="Draft":
            dpo = abspath(join(content_folder, "_drafts"))
            status = "draft"
        else:
            print("WARNING folder unknow:", page["title"])
            continue
        if page["children"]:
            folder = page["title"]
            for child in page["children"]:
                child_id = child["id"]
                child_title = child["title"]
                # print(111, child_title)

                res_t = readDatabase(databaseId=child_id,
                                     notion_header=headers,
                                     print_res=False)
                front_matter = {"title": child_title,
                                "page_id": child_id,
                                "status": status
                                }
                md = pageid_2_md(front_matter, res_t)
                fp = abspath(join(dpo, f"{child_id}.md"))
                # fn = replace_invalid_characters(f"{folder}_{child_id}.md")
                # print("writting fp", fp)
                with open(fp, 'w', encoding="utf-8") as fo:
                    fo.write(md)


def build_local():
    podcast_dir = join(www_folder_dev,"player","web")
    if not Path(podcast_dir).exists():
        Path(podcast_dir).mkdir(parents=True, exist_ok=True)
    make_podcast(abspath(join(podcast_dir,"feed_new2.xml")))
    if check_install():
        r = subprocess.run(["pelican","content","-t","static/theme","-o",www_folder_dev,"-s", pelican_local_fp])
        print(r)

        # make_ssh_config(www_folder_dev)
        # make_all_vcards_html(www_folder_dev)
        # make_all_ipynb(www_folder_dev)


def build_and_deploy():
    if check_install():
        subprocess.run(["pelican","content","-t","theme","-o",www_folder_nas,"-s","publishconf.py"])
        make_ssh_config(www_folder_nas)
        make_all_vcards_html(www_folder_nas)
        make_all_ipynb(www_folder_nas)
        # if below fails
        # run
        # > scp -rp public/* entolusis@mattnas2:/volume1/web
        cmd = ["scp", "-rp" ,f"{www_folder_nas}/*", "matt@mattnas2:/volume1/web"]
        print("cmd used", cmd)
        #result =  subprocess.run(cmd)
        from subprocess import Popen, PIPE
        proc = Popen(cmd, stdin=PIPE).wait(timeout=30)
        # proc.stdin.write('Oberron9\n')
        # proc.stdin.flush()

        if proc != 0:
            print("/!\ /!\ /!\ /!\ FAILED to SCP")
        else:
            print("SCP OK!!!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--staging",
                        help="build staging and deploy it",
                        action="store_true")    
    parser.add_argument("-l", "--local",
                        help="build site locally",
                        action="store_true")
    parser.add_argument("-g", "--git_hub",
                        help="build site for the github workflow",
                        action="store_true")
    parser.add_argument("-n", "--notion",
                        help="update notion local cache",
                        action="store_true")
    parser.add_argument("-p", "--podcast",
                        action="store_true",
                        help="wrapper for podcast")
    parser.add_argument("-t", "--tmp",
                        action="store_true",
                        help="rebuild tmp folder")

    args = parser.parse_args()
    build_flow = "win"
    pelican_overloads = None
    if args.local:
        print("BUILD DEV LOCALLY")
        # pelican_overloads = "-e FEED_DOMAIN=\"'http://localhost:8000'\""
        # pelican_overloads = "SITEURL=\"'http://localhost:5000'\" FEED_DOMAIN=\"'http://localhost:4000'\""
        pelican_overloads = "SITEURL=\"http://localhost:8000\""
    elif args.staging:
        print("BUILDING for STAGING SERVER")
    elif args.git_hub:
        print("BUILDING for GITHUB ACTIONS and gh-pages")
        build_flow = "gh"
        pelican_overloads = "SITEURL=\"https://oberron.github.io/spark-fi/\""
    else:
        print("SELECT AN OPTION !!!")
    if args.local or args.git_hub:
        dp_content = "content"
        dp_www = www_folder_dev
        theme = "theme"
    elif args.deploy:
        print("BUILDING for NAS")
        # build_and_deploy()

    if args.podcast:
        dpo = abspath(join(pelican_local_fp, podcast_dir))
        fpo = abspath(join(dpo, podcast_rss_fn))
        make_podcast(fpo=fpo, dpo=dpo)

    print("FIX image paths")

    dp_content_tmp = pre_pelican(dp_content, theme, dp_www,
                                 build_flow=build_flow,
                                 rebuild_tmp=args.tmp,
                                 rebuild_notion=args.notion,
                                 dp_not=dp_notion)
    dp_content_tmp = abspath(join(__file__, pardir, "tmp"))
    pelican_results = pelican_wrapper(dp_content_tmp, theme, dp_www,
                                      test_requirements=True,
                                      pelican_e=pelican_overloads)
    post_pelican(dp_content, theme, dp_www, pelican_results)
