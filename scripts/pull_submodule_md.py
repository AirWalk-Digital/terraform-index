import argparse
import os
import sys
from git import Repo
import logging



def create_for_azure(new_subfolder_path, args):
    meta_template_path = None
    new_meta_name = None
    if args.docker:
        meta_template_path = "../azure/template/docker_meta.template.json"
        new_meta_name = "docker_meta.json"
    if args.vm:
        meta_template_path = "../azure/template/image_meta.template.json"
        new_meta_name = "image_meta.json"

    meta_template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), meta_template_path)

    print(meta_template_path)

    ori_text = None
    with open(meta_template_path,'r') as f:
        ori_text = f.read()


    os.environ["SUBMODULE_PATH"] = f"../../submodules/{args.submod_name}"

    new_text = os.path.expandvars(ori_text)

    print(new_text)

    new_meta_path = os.path.join(new_subfolder_path, new_meta_name)

    with open(new_meta_path,'w') as f:
        f.write(new_text)
    print(f"New Meta file {new_meta_path} has been created !")



def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--repodir', required=True, metavar='repo_dir', 
        help="dir of git repo")

    args = parser.parse_args()

    repo = Repo(args.repodir)

    for submodule in repo.submodules:
        submodule.update(init=True)
        sub_repo = submodule.module()
        sub_repo.git.checkout('master')
        o = sub_repo.remotes.origin
        o.pull()

logging.basicConfig()
logging.root.setLevel(logging.INFO)
    
if __name__ == "__main__":
    main()