import os
import sass
import shutil
import time
import glob


class Builder:
    def __init__(self):
        # Create a temporary folder to write the build to, so we can rollback at any time
        self.tmp_dir = f'tmp_{int(time.time())}'
        os.mkdir(self.tmp_dir, 0o755)
        self.build_styles()

    def build_styles(self):
        os.mkdir(f'{self.tmp_dir}/styles')
        if glob.glob('static/styles/*.sass') or glob.glob('static/styles/*.scss'):
            sass.compile(dirname=('static/styles/', f'{self.tmp_dir}/styles/'))
        for file in os.listdir('static/styles/'):
            if file.endswith('.css'):
                shutil.copy(f'static/styles/{file}', f'{self.tmp_dir}/styles/')

