import os
import json
from pathlib import Path
from typing import Optional

import tools.cleaning as cm
import tools.messages as msg
import tools.fileoperations as fo

from clients import GitHubApi, LineageOsApi, ParanoidAndroidApi

from configs import Config as cfg


class AssetCollector:
    """Asset collector."""

    _root: Path = cfg.DIR_ROOT
    _dir_assets: Path = Path(_root, cfg.DIR_ASSETS)

    def __init__(
        self,
        codename: str,
        rom: str,
        chroot: str,
        clean: bool,
        rom_only: bool,
        extra_assets: Optional[bool] = False,
        ksu: Optional[bool] = False
    ) -> None:
        self._codename = codename
        self._rom = rom
        self._chroot = chroot
        self._extra_assets = extra_assets
        self._clean = clean
        self._rom_only = rom_only
        self._ksu = ksu

    def run(self) -> None:
        msg.banner("zero asset collector")
        os.chdir(self._root)
        self._check()
        os.chdir(self._dir_assets)
        # determine which SU manager and ROM are required
        su_manager = "tiann/KernelSU" if self._ksu else "topjohnwu/Magisk"
        rom_collector_dto = ""
        if self._rom == "los":
            rom_collector_dto = LineageOsApi(self._codename, self._rom_only)
        else:
            rom_collector_dto = ParanoidAndroidApi(self._codename, self._rom_only)
        # process the "ROM-only" download
        if self._rom_only:
            fo.download(rom_collector_dto.run())
            print("\n", end="")
            msg.done("ROM-only asset collection complete!")
        # process the non-"RON-only" download
        else:
            assets = [
                rom_collector_dto.run(),
                GitHubApi(
                    project=su_manager,
                    assetdir=self._dir_assets,
                    file_filter=".apk"
                ).run(),
                GitHubApi(
                    project="seppzer0/Disable_Dm-Verity_ForceEncrypt",
                    assetdir=self._dir_assets
                ).run(),
                GitHubApi(
                    project="klausw/hackerskeyboard",
                    assetdir=self._dir_assets,
                    file_filter=".apk"
                ).run(),
                GitHubApi(
                    project="aleksey-saenko/TTLChanger",
                    assetdir=self._dir_assets,
                    file_filter=".apk"
                ).run(),
                GitHubApi(
                    project="ukanth/afwall",
                    assetdir=self._dir_assets,
                    file_filter=".apk"
                ).run(),
                GitHubApi(
                    project="emanuele-f/PCAPdroid",
                    assetdir=self._dir_assets,
                    file_filter=".apk"
                ).run(),
                GitHubApi(
                    project="nfcgate/nfcgate",
                    assetdir=self._dir_assets,
                    file_filter=".apk"
                ).run(),
                "https://store.nethunter.com/NetHunter.apk",
                "https://store.nethunter.com/NetHunterKeX.apk",
                "https://store.nethunter.com/NetHunterStore.apk",
                "https://store.nethunter.com/NetHunterTerminal.apk",
                "https://eu.dl.twrp.me/cheeseburger_dumpling/twrp-3.7.0_12-1-cheeseburger_dumpling.img",
                "https://kali.download/nethunter-images/current/rootfs/kalifs-arm64-{}.tar.xz".format(self._chroot),
                "https://github.com/mozilla-mobile/firefox-android/releases/download/fenix-v117.1.0/fenix-117.1.0-arm64-v8a.apk",
                "https://f-droid.org/F-Droid.apk",
            ]
            # read extra assets from JSON file
            if self._extra_assets:
                extra_json = Path(self._root, self._extra_assets)
                if extra_json.is_file():
                    print("\n", end="")
                    msg.note("Applying extra assets..")
                    with open(extra_json) as f:
                        data = json.load(f)
                        # validate the input JSON
                        rootkeys = ("github", "local", "other")
                        if not all(le in data.keys() for le in rootkeys):
                            msg.error(
                                "Incorrect JSON syntax detected."
                                "Allowed keys: 'github', 'local', 'other' ."
                            )
                        # append extra asset data
                        for k in rootkeys:
                            if data[k]:
                                for e in data[k]:
                                    if k == "github":
                                        assets.append(GitHubApi(e))
                                    else:
                                        assets.append(e)
                    msg.done("Extra assets added!")
                    print("\n", end="")
            # collect all the specified assets into single directory
            nhpatch = "nhpatch.sh"
            fo.ucopy(
                Path(self._root, "modifications", nhpatch),
                Path(self._dir_assets, nhpatch)
            )
            for e in assets:
                if e:
                    fo.download(e)
            print("\n", end="")
            msg.done("Assets collected!")
        os.chdir(self._root)

    def _check(self) -> None:
        """Initiate some checks before execution."""
        os.chdir(self._root)
        # directory check
        if not self._dir_assets.is_dir():
            os.mkdir(self._dir_assets)
        else:
            if len(os.listdir(self._dir_assets)) != 0:
                cmsg = f'[ ? ] Found an existing "{self._dir_assets.name}" folder, clean it? [Y/n]: '
                ans = input(cmsg).lower() if not self._clean else "y"
                match ans:
                    case "y":
                        msg.note("Cleaning 'assets' directory..")
                        os.chdir(self._dir_assets)
                        cm.remove("./*")
                        os.chdir(self._root)
                        msg.done("Done!")
                    case "n":
                        msg.cancel("Cancelling asset download.")
                    case _:
                        msg.error("Invalid option selected.")
        print("\n", end="")
