# HydrusYTDLProxy
A thing to allow to use YouTube-dlp with Hydrus Network

### Run
```shell
fastapi run main.py
```

### Server Deployment
Coolify:
1. Add as <kbd>NIXPACK</kbd>
2. Set start command to `fastapi run main.py --port=4458`
3. Set network port to `4458`.


### Install
macOS:
```shell
pip install opencv-python qtpy

# pip install git+https://github.com/hydrusnetwork/hydrus.git#egg=hydrus&subdirectory=hydrus
pip install git+https://github.com/luckydonald-forks/hydrus.git
```