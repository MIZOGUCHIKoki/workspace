# operate_netCDF
- Contributor
    - MIZOGUCHI Koki(Kochi University of Technology, Japan.)
    - YAJIMA Risa(Ibaraki University, Japan.)
- Created at
    - Mon Oct. 21, 2024.
- Data resources
    - [GFED5 gruidded files](https://www.globalfiredata.org/data.html) Accessed-on: Oct. 21, 2024.
# Environment construction for `netCDF4`?
The following is an example of the construction of the environment for macOS.
Enter the examples in `Terminal.app`.

1. Install `brew` if your machine doesn't have it. (`brew` is a package management system.)
    ```bash
    $ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```
1. Install `hdf5` and `netCDF4` via `brew`.
    ```bash
    $ brew install hdf5
    $ brew install netCDF4
    ```
1. Set up your Python environment.
    1. Check whether you can use `python3` and `pip3` on your Mac.
        ```bash
        $ which python3
        $ which pip3
        ```
        - If the following message appears, install the package via `brew`.
            ```bash
            $ which [package]
            [package] not found.
            ```
    1. Activate Python virtual environment on your machine.
        ```bash
        $ python3 -m venv ~/local_python
        $ source ~/local_python/bin/activate
        ```
        (And then, the prompt will change.)
    1. Install `netCDF4` via `pip3`.
        ```bash
        $ pip3 install netCDF4
        ```
1. Check whether you can use `netCDF4` in Python code.
    ```bash
    $ python3
    >>> from netCDF4 import Dataset
    ```
    If no any errors, You may success to construct the environment.
1. When you break from the virtual environment, enter the following command.
    ```bash
    $ deactivate
    ```
# Notes
1. netCDF ファイルから，緯度・経度・時間・炭素(C)を取り出す．
1. 1⽇単位の，全ての経度・緯度の炭素のデータを⾜す．（31日分）
1. 1⽇ごとの全世界の積算量を，CSVファイルとして保存する．
1. 時系列表を作る．

