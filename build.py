import os
import platform
import shutil
import sys
import urllib.request
import zipfile

DOWNLOAD_URL = "https://github.com/RenderKit/oidn/releases/download/v{MAJOR}.{MINOR}.{PATCH}/{filename}"

FILE_NAME = "oidn-{MAJOR}.{MINOR}.{PATCH}.{arch}.{os}.{ext}"

DOWNLOAD_TYPES = {"windows": "zip"}


def get_os_information():
    """Get the os name and the architecture.

    Returns:
        tuple: OS name and architecture.
    """
    os_names = {"Windows": "windows"}
    architectures = {"AMD64": "x64"}
    os_platform = platform.system()
    os_architecture = platform.machine()

    return (
        os_names.get(os_platform, "linux"),
        architectures.get(os_architecture, "x64"),
    )


def build(source_path, build_path, install_path, targets):
    """Build/Install function.

    Args:
        source_path (str): Path to the rez package root.
        build_path (str): Path to the rez build directory.
        install_path (str): Path to the rez install directory.
        targets (str): Target run by the command, i.e. `build`, `install`...

    Raises:
        RuntimeError: Your current OS is not supported.
    """
    os_name, arch = get_os_information()
    package_major, package_minor, package_patch = os.environ.get(
        "REZ_BUILD_PROJECT_VERSION", "0.0.0"
    ).split(".")

    if os_name in ("linux", "Darwin"):
        raise RuntimeError(f"Your current OS is not supported ({os_name}).")

    oidn_archive = FILE_NAME.format(
        MAJOR=package_major,
        MINOR=package_minor,
        PATCH=package_patch,
        os=os_name,
        arch=arch,
        ext=DOWNLOAD_TYPES.get(os_name),
    )
    download_url = DOWNLOAD_URL.format(
        MAJOR=package_major, MINOR=package_minor, PATCH=package_patch, filename=oidn_archive
    )

    def _build():
        """Build the package locally."""
        archive_path = os.path.join(build_path, oidn_archive)

        if not os.path.isfile(archive_path):
            print(f"Downloading OIDN archive from: {download_url}")
            
            download_request = urllib.request.Request(
                url=download_url,
                headers={'User-Agent': 'Mozilla/5.0'},
            )

            with open(archive_path, "wb") as file:
                with urllib.request.urlopen(download_request) as request:
                    file.write(request.read())

        print("Extracting the archive.")
        match os_name:
            case "windows":
                with zipfile.ZipFile(archive_path) as archive_file:
                    archive_file.extractall(build_path)

            case "macos":
                pass
            case _:
                pass

    def _install():
        """Install the package."""
        print("Installing the package.")
        extracted_archive_path = os.path.join(
            build_path, "oidn-2.3.1.x64.windows"
        )
        install_directory = os.path.join(install_path, "oidn")

        if os.path.isdir(install_directory):
            shutil.rmtree(install_directory)
        os.mkdir(install_directory)

        match os_name:
            case "windows":
                for element in os.listdir(extracted_archive_path):
                    element_path = os.path.join(extracted_archive_path, element)
                    shutil.move(element_path, install_directory)
            case "macos":
                pass
            case _:
                pass

    _build()

    if "install" in (targets or []):
        _install()


if __name__ == "__main__":
    build(
        source_path=os.environ["REZ_BUILD_SOURCE_PATH"],
        build_path=os.environ["REZ_BUILD_PATH"],
        install_path=os.environ["REZ_BUILD_INSTALL_PATH"],
        targets=sys.argv[1:],
    )
