# Copyright (c) 2025 Ahmed Ayyad (ahmedyad200)
# Licensed under Custom Proprietary License
# Redistribution and resale are prohibited.

import os
import shutil
import subprocess
import tempfile


def update_bot():
    try:
        repo_url = f"https://github.com/ahmedayyad-dev/Template-Bot-for-EHkBot.git"

        local_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        temp_dir = tempfile.mkdtemp()

        try:
            env = os.environ.copy()
            env['GIT_TERMINAL_PROMPT'] = '0'
            env['GIT_ASKPASS'] = 'echo'

            result = subprocess.run(
                ['git', 'clone', '--branch', 'master', '--single-branch', repo_url, temp_dir],
                env=env,
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                return False

            for item in os.listdir(temp_dir):
                if item == '.git':
                    continue

                src = os.path.join(temp_dir, item)
                dst = os.path.join(local_path, item)

                if os.path.exists(dst):
                    if os.path.isdir(dst):
                        shutil.rmtree(dst)
                    else:
                        os.remove(dst)

                if os.path.isdir(src):
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)

            return True

        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    except Exception as e:
        return False